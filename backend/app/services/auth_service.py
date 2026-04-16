from app.utils.security import hash_password, generate_token, verify_password, create_access_token
from datetime import datetime, timedelta
from app.models.auth import User, EmailVerification, ResetPasswordToken
from fastapi import HTTPException, status

def register_user(db, email, password):
    existing_user = db.query(User).filter(User.email == email).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
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

def verify_email_token(db, token: str):
    verification = (
        db.query(EmailVerification)
        .filter(EmailVerification.token == token)
        .first()
    )

    if not verification:
        raise HTTPException(status_code=400, detail="Invalid token")

    if verification.is_used:
        raise HTTPException(status_code=400, detail="Token already used")

    if verification.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Token expired")

    user = db.query(User).filter(User.id == verification.user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # activate user
    user.is_verified = True
    verification.is_used = True

    db.commit()

    return user



def login_user(db, email, password):
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.is_verified:
        raise HTTPException(status_code=400, detail="Email not verified")

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
        raise HTTPException(status_code=400, detail="Invalid token")

    if reset.is_used:
        raise HTTPException(status_code=400, detail="Token already used")

    if reset.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Token expired")

    user = reset.user

    user.hashed_password = hash_password(new_password)
    reset.is_used = True

    db.commit()
    
    
def request_new_verification_email(db, email):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return  # silent (security)
    
    if user.is_verified:
        return  # silent (security)

    token = generate_token()

    verification = EmailVerification(
        user_id=user.id,
        token=token,
        expires_at=datetime.utcnow() + timedelta(hours=24)
    )
    db.add(verification)
    db.commit()
    return user, token