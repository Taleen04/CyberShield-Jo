from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Boolean, 
    Float, ForeignKey, Enum as SQLEnum, JSON
)
from sqlalchemy.orm import relationship
import enum
from app.database import Base

class UserRole(str, enum.Enum):
    """User role enumeration"""
    USER = "user"
    ADMIN = "admin"


class InputType(str, enum.Enum):
    """Type of input being analyzed or reported"""
    URL = "url"
    PHONE = "phone"
    TEXT_MESSAGE = "text_message"


class ThreatCategory(str, enum.Enum):
    """Threat risk categories"""
    SAFE = "safe"  # 0-30%
    SUSPICIOUS = "suspicious"  # 31-70%
    HIGH_RISK = "high_risk"  # 71-100%
    NO_DATA = "no_data"  # When no data is available


class ReportStatus(str, enum.Enum):
    """Status of user-submitted reports"""
    UNDER_REVIEW = "under_review"
    VERIFIED_SCAM = "verified_scam"
    SAFE = "safe"


class URLClassification(str, enum.Enum):
    """URL reputation classification"""
    LEGITIMATE = "legitimate"
    MALICIOUS = "malicious"