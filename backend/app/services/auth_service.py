from app.utils.security import hash_password, generate_token, verify_password, create_access_token
from datetime import datetime, timedelta
from app.models.user import User, EmailVerification, ResetPasswordToken


def register_user(db, email, password):
    hashed = hash_password(password)

    user = User(email=email, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)

    token = generate_token()

    verification = EmailVerification(
        user_id=user.id,
        token=token,
        expires_at=datetime.utcnow() + timedelta(hours=24)
    )
    db.add(verification)
    db.commit()

    return user, token


def login_user(db, email, password):
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.hashed_password):
        raise Exception("Invalid credentials")

    if not user.is_verified:
        raise Exception("Email not verified")

    token = create_access_token({"sub": str(user.id)})

    return token, user


def forgot_password(db, email):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return  # silent (security)

    token = generate_token()

    reset = ResetPasswordToken(
        user_id=user.id,
        token=token,
        expires_at=datetime.utcnow() + timedelta(minutes=15)
    )

    db.add(reset)
    db.commit()

    return token


def reset_password(db, token, new_password):
    reset = db.query(ResetPasswordToken).filter(
        ResetPasswordToken.token == token
    ).first()

    if not reset:
        raise Exception("Invalid token")

    if reset.is_used:
        raise Exception("Token already used")

    if reset.expires_at < datetime.utcnow():
        raise Exception("Token expired")

    user = reset.user

    user.hashed_password = hash_password(new_password)
    reset.is_used = True

    db.commit()
    
    
