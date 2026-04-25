from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, Field, field_validator
from app.models.lookup import ThreatCategory, InputType
import re


# ──────────────────────────────────────────────
# REQUEST SCHEMAS
# ──────────────────────────────────────────────

class ScanURLRequest(BaseModel):
    url: str = Field(..., min_length=1, max_length=2048, description="The URL to analyze")

    @field_validator("url")
    @classmethod
    def validate_url_format(cls, v: str) -> str:
        v = v.strip()

        if not v:
            raise ValueError("URL cannot be empty")

        if len(v) > 2048:
            raise ValueError("URL too long")
        
        if not v.startswith(("http://", "https://")):
            raise ValueError("URL must start with 'http://' or 'https://'")
        
        # Basic sanity check: no spaces or control chars
        if re.search(r'[\s\x00-\x1f]', v):
            raise ValueError("URL contains invalid characters")

        return v

    model_config = {
        "json_schema_extra": {
            "example": {"url": "https://suspicious-site.example.com/offer"}
        }
    }


class ScanPhoneRequest(BaseModel):
    phone_number: str = Field(..., description="Phone number in E.164 or local format")

    @field_validator("phone_number")
    @classmethod
    def validate_phone_format(cls, v: str) -> str:
        # Accept E.164 (+962XXXXXXXXX) or digits-only (7-15 digits)
        pattern = re.compile(r'^\+?[1-9]\d{6,14}$')
        if not pattern.match(v):
            raise ValueError("Invalid phone number format. Use E.164 format (e.g. +962799123456)")
        return v

    model_config = {
        "json_schema_extra": {
            "example": {"phone_number": "+962799123456"}
        }
    }


class ScanTextRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000, description="The text message to analyze")
    phone_number: Optional[str] = Field(None, description="Optional sender phone number")
    message_source: Optional[str] = Field(default="sms", description="optional source of the message (e.g. sms, email)")

    @field_validator("phone_number")
    @classmethod
    def validate_phone_optional(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        pattern = re.compile(r'^\+?[1-9]\d{6,14}$')
        if not pattern.match(v):
            raise ValueError("Invalid phone number format. Use E.164 format (e.g. +962799123456)")
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "Congratulations! You've won a free iPhone. Click here: http://scam.example.com",
                "phone_number": "+962799123456",
                "message_source": "sms"
            }
        }
    }


# ──────────────────────────────────────────────
# RESPONSE SCHEMAS
# ──────────────────────────────────────────────

class ScanResult(BaseModel):
    scan_id: int
    final_category: ThreatCategory
    ml_risk_score: Optional[float] = None
    ml_probabilities: Optional[dict[str, float]] = None
    explanation: str
    contributing_factors: list[str]
    analysis_details: Optional[dict[str, Any]]

    model_config = {"from_attributes": True}


class ScanHistoryItem(BaseModel):
    id: int
    input_type: InputType
    input_value: str
    threat_category: ThreatCategory
    created_at: datetime

    model_config = {"from_attributes": True}


class ScanHistoryResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: list[ScanHistoryItem]
