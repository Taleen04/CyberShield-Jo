from sqlalchemy import (
    Column, Index, Integer, String, Text, DateTime, Boolean, 
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
    threat_category = Column(SQLEnum(ThreatCategory), nullable=False)
    
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
    phone_number_id = Column(
        Integer,
        ForeignKey("phone_numbers.id", ondelete="SET NULL"),
        nullable=True
    )
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False, index=True)

    # Relationships
    user = relationship("User", back_populates="scans")
    phone_number = relationship(
        "PhoneNumber",
        back_populates="scans"
    )
    __table_args__ = (
        Index("idx_scans_user_created", "user_id", "created_at"),
    )
    
    
class Report(Base):
    """User-submitted reports (both post-analysis and manual)"""
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Report content
    input_type = Column(SQLEnum(InputType), nullable=False)
    input_value = Column(Text, nullable=False)
    notes = Column(Text, nullable=True)  # Optional user comments
    location_inside_jordan = Column(Boolean, nullable=True)
    admin_added = Column(Boolean, nullable=False)
    
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
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)

    # Relationships
    scan = relationship("Scan")
    user = relationship(
        "User",
        back_populates="reports",
        foreign_keys=[user_id]
    )

    reviewer = relationship(
        "User",
        back_populates="reviewed_reports",
        foreign_keys=[reviewed_by_admin_id]
    )
    __table_args__ = (
        Index("idx_reports_user_status", "user_id", "status"),
    )
    
    
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
    scans = relationship("Scan", back_populates="phone_number")

    @property 
    def spam_rate(self) -> float:
        if self.total_reports == 0:
            return 0.0
        return round(self.spam_reports / self.total_reports, 4) 