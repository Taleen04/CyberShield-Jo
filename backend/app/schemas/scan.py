from datetime import datetime
from pydantic import BaseModel, Field
from app.models.lookup import ThreatCategory, InputType


class ScanTextRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000, description="The SMS text to classify")
    phone_number: str | None = Field(None, description="Optional sender phone number for tracking")
    message_source: InputType = Field("sms", description="Source of the message, e.g. 'sms', 'email', etc.")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "Congratulations! You've won a free iPhone. Click here to claim.",
                "phone_number": "+962799123456",
                "message_source": "sms"
            }
        }
    }


class ScanTextResponse(BaseModel):
    label: ThreatCategory  # "spam" or "ham"
    log_id: int             # ID of the PredictionLog row created