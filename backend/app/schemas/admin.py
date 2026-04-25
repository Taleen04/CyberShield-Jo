"""
schemas/admin.py
----------------
Pydantic request / response models for admin endpoints.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.lookup import InputType, ReportStatus


# ──────────────────────────────────────────────
# Shared / reusable
# ──────────────────────────────────────────────

class PaginationMeta(BaseModel):
    """Metadata attached to every paginated response."""

    page: int
    limit: int
    total: int
    total_pages: int


# ──────────────────────────────────────────────
# GET /admin/reports
# ──────────────────────────────────────────────

class AdminReportListItem(BaseModel):
    """Single row in the admin reports list."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    input_type: InputType
    input_value: str
    status: ReportStatus
    notes: Optional[str] = None
    admin_notes: Optional[str] = None
    location_inside_jordan: Optional[bool] = None
    admin_added: bool

    # Metadata
    user_id: int
    scan_id: Optional[int] = None
    reviewed_by_admin_id: Optional[int] = None
    reviewed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    analysis_result: Optional[Any] = None


class PaginatedAdminReports(BaseModel):
    """Paginated wrapper for admin report list."""

    items: list[AdminReportListItem]
    meta: PaginationMeta


# ──────────────────────────────────────────────
# PATCH /admin/reports/{report_id}/status
# ──────────────────────────────────────────────

class UpdateReportStatusRequest(BaseModel):
    """Body for updating a report's status."""

    new_status: ReportStatus = Field(
        ...,
        description="Target status. Must be 'verified_scam' or 'safe'.",
    )
    admin_notes: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Optional note recorded alongside the status change.",
    )


class UpdateReportStatusResponse(BaseModel):
    """Returned after a successful status update."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    old_status: ReportStatus
    new_status: ReportStatus
    reviewed_by_admin_id: int
    reviewed_at: datetime
    admin_notes: Optional[str] = None


# ──────────────────────────────────────────────
# POST /admin/reports  (admin-initiated blacklist entry)
# ──────────────────────────────────────────────

class AdminAddReportRequest(BaseModel):
    """Body for admin-created blacklist entries (US-18)."""

    input_type: InputType = Field(..., description="url | phone | text_message")
    input_value: str = Field(..., min_length=1, max_length=2048)
    threat_category: ReportStatus = Field(
        ...,
        description="'verified_scam' or 'safe'. Cannot be 'under_review'.",
    )
    admin_notes: Optional[str] = Field(default=None, max_length=1000)


class AdminAddReportResponse(BaseModel):
    """Returned after an admin-created report is persisted."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    input_type: InputType
    input_value: str
    status: ReportStatus
    admin_added: bool
    admin_notes: Optional[str] = None
    created_at: datetime


# ──────────────────────────────────────────────
# GET /admin/metrics
# ──────────────────────────────────────────────

class ScanBreakdown(BaseModel):
    """Scan counts split by input type."""

    url: int = 0
    phone: int = 0
    text_message: int = 0


class ThreatBreakdown(BaseModel):
    """Scan counts split by threat category verdict."""

    safe: int = 0
    suspicious: int = 0
    high_risk: int = 0
    no_data: int = 0


class ReportStatusBreakdown(BaseModel):
    """Report counts split by review status."""

    under_review: int = 0
    verified_scam: int = 0
    safe: int = 0


class ReportOriginBreakdown(BaseModel):
    """Report counts split by who created them."""

    user_submitted: int = 0
    admin_added: int = 0


class DailyCount(BaseModel):
    """Single data-point in a time-series — one calendar date and its count."""

    date: str = Field(..., description="ISO date string, e.g. '2024-07-21'")
    count: int


class TopThreatEntry(BaseModel):
    """Most-reported input values across the entire system."""

    input_type: InputType
    input_value: str
    report_count: int


class ScanMetrics(BaseModel):
    """Everything derived from the scans table."""

    total: int
    today: int
    last_7_days: int
    last_30_days: int
    by_input_type: ScanBreakdown
    by_threat_category: ThreatBreakdown
    average_ml_confidence: Optional[float] = Field(
        default=None,
        description="Mean ML confidence score across all scans that have one (0–100).",
    )
    daily_last_7_days: list[DailyCount] = Field(
        default_factory=list,
        description="Per-day scan counts for the last 7 calendar days.",
    )


class ReportMetrics(BaseModel):
    """Everything derived from the reports table."""

    total: int
    today: int
    last_7_days: int
    last_30_days: int
    pending_review: int = Field(
        ..., description="Reports currently in 'under_review' state."
    )
    by_status: ReportStatusBreakdown
    by_input_type: ScanBreakdown          # same shape, reused
    by_origin: ReportOriginBreakdown
    daily_last_7_days: list[DailyCount] = Field(
        default_factory=list,
        description="Per-day report counts for the last 7 calendar days.",
    )


class PhoneMetrics(BaseModel):
    """Summary stats from the phone_numbers table."""

    total_tracked: int
    average_spam_rate: Optional[float] = Field(
        default=None,
        description="Mean spam rate across all tracked phone numbers (0–1).",
    )


class SystemMetricsResponse(BaseModel):
    """
    Full system activity dashboard payload (US-19).

    Groups metrics by domain so the frontend can render each card independently.
    """

    generated_at: datetime = Field(
        ..., description="UTC timestamp when these metrics were computed."
    )
    scans: ScanMetrics
    reports: ReportMetrics
    phone_numbers: PhoneMetrics
    top_threats: list[TopThreatEntry] = Field(
        default_factory=list,
        description="Top 10 most-reported input values across the whole system.",
    )
