from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, Field
from app.models.lookup import InputType, ReportStatus


# ──────────────────────────────────────────────
# REQUEST SCHEMAS
# ──────────────────────────────────────────────

class ReportFromScanRequest(BaseModel):
    """Submit a report linked to an existing scan result."""
    scan_id: int = Field(..., description="ID of the scan this report is based on")
    notes: Optional[str] = Field(None, max_length=2000, description="Optional user comments")
    location_inside_jordan: Optional[bool] = Field(default=True, description="Whether the incident occurred inside Jordan")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "scan_id": 42,
                "notes": "Received this message from an unknown number claiming to be my bank.",
                "location_inside_jordan": "True"
            }
        }
    }


class ManualReportRequest(BaseModel):
    """Submit a report without prior analysis."""
    input_type: InputType = Field(..., description="Type of the reported input")
    input_value: str = Field(..., min_length=1, max_length=2048, description="The URL, phone number, or message text")
    location_inside_jordan: bool = Field(..., description="Whether the incident occurred inside Jordan")
    notes: Optional[str] = Field(None, max_length=2000, description="Optional user comments")

    model_config = {
        "json_schema_extra": {
            "example": {
                "input_type": "phone",
                "input_value": "+962799123456",
                "location_inside_jordan": True,
                "notes": "This number called me claiming to offer a bank loan."
            }
        }
    }


# ──────────────────────────────────────────────
# RESPONSE SCHEMAS
# ──────────────────────────────────────────────

class ReportResponse(BaseModel):
    id: int
    input_type: InputType
    input_value: str
    notes: Optional[str]
    scan_id: Optional[int]
    status: ReportStatus
    created_at: datetime

    model_config = {"from_attributes": True}


class MyReportItem(BaseModel):
    id: int
    input_type: InputType
    input_value: str
    created_at: datetime
    status: ReportStatus

    model_config = {"from_attributes": True}
