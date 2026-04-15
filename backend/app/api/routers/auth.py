from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.auth_service import register_user, login_user, forgot_password, reset_password
from app.database import get_db
from app.services.email_service import send_verification_email, send_reset_email
from app.schemas.auth import RegisterRequest, LoginRequest, ForgotPasswordRequest, ResetPasswordRequest


router = APIRouter(prefix="", tags=["Authentication"])

@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    user, token = register_user(db, data.email, data.password)
    send_verification_email(user.email, token)
    return {"message": "Registration successful",
            "user": {
    "id": user.id,
    "email": user.email,
    "is_verified": user.is_verified,
    "created_at": user.created_at
  }}


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    token, user = login_user(db, data.email, data.password)
    return {
        "access_token": token,
        "token_type": "bearer"
    }
    
    
@router.post("/forgot-password")
def forgot(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    token = forgot_password(db, data.email)

    if token:
        send_reset_email(data.email, token)

    return {"message": "If an account exists, a reset link has been sent"}


@router.post("/reset-password")
def reset(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    reset_password(db, data.token, data.new_password)
    return {"message": "Password reset successful"}