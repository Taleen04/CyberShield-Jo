from datetime import datetime
from pydantic import BaseModel, Field


# ── Prediction ──────────────────────────────────────────────

class PredictRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000, description="The SMS text to classify")
    phone_number: str | None = Field(None, description="Optional sender phone number for tracking")
    message_source: str = Field("sms", description="Source of the message, e.g. 'sms', 'email', etc.")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "Congratulations! You've won a free iPhone. Click here to claim.",
                "phone_number": "+962799123456",
                "message_source": "sms"
            }
        }
    }


class PredictResponse(BaseModel):
    label: str              # "spam" or "ham"
    confidence: float       # 0.0 → 1.0
    phone_number: str | None
    log_id: int             # ID of the PredictionLog row created


# ── Phone Number Reports ─────────────────────────────────────

class PhoneNumberSummary(BaseModel):
    id: int
    number: str
    total_reports: int
    spam_reports: int
    ham_reports: int
    spam_rate: float
    first_seen: datetime
    last_seen: datetime

    model_config = {"from_attributes": True}


class PredictionLogOut(BaseModel):
    id: int
    message_text: str
    predicted_label: str
    confidence: float
    created_at: datetime

    model_config = {"from_attributes": True}


class PhoneNumberDetail(PhoneNumberSummary):
    predictions: list[PredictionLogOut] = []