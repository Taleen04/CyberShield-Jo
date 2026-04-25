from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.auth_service import register_user, login_user, forgot_password, reset_password
from app.database import get_db
from app.services.email_service import send_verification_email, send_reset_email
from app.services.auth_service import verify_email_token, request_new_verification_email
from app.schemas.auth import RegisterRequest, LoginRequest, ForgotPasswordRequest, ResetPasswordRequest, EmailVerificationRequest
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


templates = Jinja2Templates(directory="app/templates")
router = APIRouter(prefix="/auth", tags=["Authentication"])

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
        "token_type": "bearer",
        "is_admin": user.role == "admin"
    }
    
    
@router.post("/forgot-password")
def forgot(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    token = forgot_password(db, data.email)

    if token:
        send_reset_email(data.email, token)

    return {"message": "If an account exists, a reset link has been sent"}


@router.get("/reset-password", response_class=HTMLResponse)
def reset_password_page(request: Request, token: str):
    return templates.TemplateResponse(
        "reset_password.html",
        {
            "request": request,
            "token": token
        }
    )
    
    
@router.post("/reset-password")
def reset(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    reset_password(db, data.token, data.new_password)
    return {"message": "Password reset successful"}


@router.get("/verify-email")
def verify_email(request: Request, token: str, db: Session = Depends(get_db)):
    try:
        verify_email_token(db, token)
        return templates.TemplateResponse("email_verification_success.html", {"request": request, "message": "Email verified successfully!"})
    
    except HTTPException as e:
        return templates.TemplateResponse(
            "email_verification_error.html",
            {"request": request, "message": str(e.detail)}
        )
        
        
@router.post("/resend-verification-email")
def resend_verification_email(data: EmailVerificationRequest, db: Session = Depends(get_db)):
    user, token = request_new_verification_email(db, data.email)
    if user and token:
        send_verification_email(user.email, token)
    return {"message": "If an account exists, a verification email has been resent"}