import re

from pydantic import BaseModel, EmailStr, Field, field_validator


def validate_password_strength(value: str) -> str:
    if len(value) < 8:
        raise ValueError("Password must be at least 8 characters long")
    if not re.search(r"[A-Z]", value):
        raise ValueError("Password must include at least one uppercase letter")
    if not re.search(r"[a-z]", value):
        raise ValueError("Password must include at least one lowercase letter")
    if not re.search(r"\d", value):
        raise ValueError("Password must include at least one digit")
    if not re.search(r"[^\w\s]", value):
        raise ValueError("Password must include at least one special character")
    return value


class ForgotPasswordRequest(BaseModel):
    email: EmailStr = Field(
        ...,
        description="User's registered email address",
        example="user@example.com"
    )


class ResetPasswordRequest(BaseModel):
    token: str = Field(
        ...,
        description="Password reset token sent via email",
        example="abc123reset-token"
    )
    
    new_password: str = Field(
        ...,
        description="New password for the user",
        example="SecurePass123!"
    )

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, value: str) -> str:
        return validate_password_strength(value)


class RegisterRequest(BaseModel):
    email: EmailStr = Field(
        ...,
        description="User's registered email address",
        example="user@example.com"
    )
    password: str = Field(
        ...,
        description="Password for the user",
        example="SecurePass123!"
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        return validate_password_strength(value)


class LoginRequest(BaseModel):
    email: EmailStr = Field(
        ...,
        description="User's registered email address",
        example="user@example.com"
    )
    password: str = Field(
        ...,
        description="Password for the user",
        example="SecurePass123!"
    )
    

class EmailVerificationRequest(BaseModel):
    email: EmailStr = Field(
        ...,
        description="User's registered email address",
        example="user@example.com"
    )
    