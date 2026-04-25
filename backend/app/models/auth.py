from datetime import datetime, timezone
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Boolean, 
    Float, ForeignKey, Enum as SQLEnum, JSON
)
from sqlalchemy.orm import relationship
import enum
from app.database import Base
from app.models.lookup import UserRole
    
class User(Base):
    """User account model"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(
        SQLEnum(UserRole, name="user_role"),
        default=UserRole.USER,
        nullable=False
    )
    is_verified = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_locked = Column(Boolean, default=False, nullable=False)  # For account locking after failed attempts
    failed_login_attempts = Column(Integer, default=0, nullable=False)
    last_failed_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)

    # Relationships
    email_verifications = relationship("EmailVerification", back_populates="user", cascade="all, delete-orphan")
    scans = relationship("Scan", back_populates="user", cascade="all, delete-orphan", lazy="selectin", order_by="desc(Scan.created_at)")
    reports = relationship(
        "Report",
        back_populates="user",
        foreign_keys="Report.user_id",
        cascade="all, delete-orphan"
    )

    reviewed_reports = relationship(
        "Report",
        back_populates="reviewer",
        foreign_keys="Report.reviewed_by_admin_id"
    )
    password_resets = relationship("ResetPasswordToken", back_populates="user", cascade="all, delete-orphan")


class EmailVerification(Base):
    """Email verification tokens"""
    __tablename__ = "email_verifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token = Column(String(255), unique=True, index=True, nullable=False)
    is_used = Column(Boolean, default=False, nullable=False)
    expires_at = Column(DateTime, nullable=False)  # 24 hours from creation
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    # Relationships
    user = relationship("User", back_populates="email_verifications")


class ResetPasswordToken(Base):
    """Password reset tokens"""
    __tablename__ = "reset_password_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    token = Column(String(255), unique=True, index=True, nullable=False)
    
    is_used = Column(Boolean, default=False, nullable=False)
    expires_at = Column(DateTime, nullable=False)  # e.g., 15–30 minutes
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    # Relationships
    user = relationship("User", back_populates="password_resets")