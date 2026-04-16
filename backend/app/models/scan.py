from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Boolean, 
    Float, ForeignKey, Enum as SQLEnum, JSON
)
from sqlalchemy.orm import relationship
import enum
from app.database import Base
from app.models.lookup import UserRole, InputType, ThreatCategory, ReportStatus, URLClassification
from datetime import datetime, timezone


class Scan(Base):
    """Analysis/Scan history for users"""
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    input_type = Column(SQLEnum(InputType), nullable=False)
    input_value = Column(Text, nullable=False)  # The URL, phone number, or text message
    
    # Risk analysis results
    ml_confidence = Column(Float, nullable=True)  # 0-100%
    threat_category = Column(SQLEnum(ThreatCategory), nullable=False) | Column(SQLEnum(URLClassification), nullable=False)
    
    # Detailed analysis results (stored as JSON for flexibility)
    analysis_details = Column(JSON, nullable=False)
    # Example structure:
    # {
    #   "ml_result": {"score": 0.8, "category": "suspicious"},
    #   "url_analysis": {"score": 0.9, "category": "high_risk", "virustotal": {...}},
    #   "phone_analysis": {"score": 0.5, "category": "suspicious"},
    #   "heuristic_result": {"score": 0.3, "indicators": [...]},
    #   "community_reports": {"count": 5, "score": 0.7},
    #   "explanation": "High risk due to...",
    #   "contributing_factors": ["url", "ml_model"]
    # }
    
    # Optional fields for text message analysis
    sender_phone_number = Column(String(50), nullable=True)  # If provided with text message
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False, index=True)

    # Relationships
    user = relationship("User", back_populates="scans")


class Report(Base):
    """User-submitted reports (both post-analysis and manual)"""
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Report content
    input_type = Column(SQLEnum(InputType), nullable=False)
    input_value = Column(Text, nullable=False)
    notes = Column(Text, nullable=True)  # Optional user comments
    location_inside_jordan = Column(Boolean, nullable=True)  # For manual reports (US-11-B)
    
    # Analysis reference (if report was made after analysis)
    scan_id = Column(Integer, ForeignKey("scans.id", ondelete="SET NULL"), nullable=True)
    analysis_result = Column(JSON, nullable=True)  # Copy of analysis result if applicable
    
    # Report status
    status = Column(SQLEnum(ReportStatus), default=ReportStatus.UNDER_REVIEW, nullable=False)
    
    # Admin review
    reviewed_by_admin_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    reviewed_at = Column(DateTime, nullable=True)
    admin_notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="reports", foreign_keys=[user_id])
    scan = relationship("Scan")
    reviewed_by = relationship("User", foreign_keys=[reviewed_by_admin_id])


class URLReputation(Base):
    """Admin-managed URL reputation database"""
    __tablename__ = "url_reputations"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(2048), unique=True, index=True, nullable=False)  # Normalized URL
    classification = Column(SQLEnum(URLClassification), nullable=False)
    
    # Metadata
    added_by_admin_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    last_updated_by_admin_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    notes = Column(Text, nullable=True)  # Admin notes about the URL
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Track changes for auditability (US-17: cannot remove entries)
    is_active = Column(Boolean, default=True, nullable=False)  # Soft delete instead of hard delete

    # Relationships
    added_by = relationship("User", foreign_keys=[added_by_admin_id])
    last_updated_by = relationship("User", foreign_keys=[last_updated_by_admin_id])
    
    
class PhoneNumber(Base):
    __tablename__ = "phone_numbers"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String(20), unique=True, index=True, nullable=False)
    total_reports = Column(Integer, default=0)
    spam_reports = Column(Integer, default=0)
    ham_reports = Column(Integer, default=0)

    first_seen = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    last_seen = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    scans = relationship("Scan", back_populates="phone_numbers")

    @property
    def spam_rate(self) -> float:
        if self.total_reports == 0:
            return 0.0
        return round(self.spam_reports / self.total_reports, 4)
