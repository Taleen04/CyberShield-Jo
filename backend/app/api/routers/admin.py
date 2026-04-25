"""
routers/admin_router.py
-----------------------
HTTP layer for all admin-only endpoints.

Routes
------
  GET   /admin/                               panel access check          (US-16)
  GET   /admin/reports                        paginated report list        (US-17)
  PATCH /admin/reports/{report_id}/status     update report status         (US-17)
  POST  /admin/reports                        admin blacklist entry        (US-18)
  GET   /admin/metrics                        system activity metrics      (US-19)
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from app.api.deps import get_current_admin
from app.api.deps import get_current_user
from app.database import get_db
from app.models.lookup import ReportStatus, UserRole
from app.models.auth import User
from app.schemas.admin import (
    AdminAddReportRequest,
    AdminAddReportResponse,
    PaginatedAdminReports,
    SystemMetricsResponse,
    UpdateReportStatusRequest,
    UpdateReportStatusResponse,
)
import os
from app.services import admin_service

router = APIRouter(prefix="/admin", tags=["Admin"])
_security = HTTPBearer()


# ──────────────────────────────────────────────────────────────────────────────
# US-16  –  Access admin panel 
# ──────────────────────────────────────────────────────────────────────────────

@router.get(
    "/",
    summary="Admin panel access check",
    description=(
        "Returns a simple confirmation that the authenticated user has admin "
        "access. Non-admin requests are rejected with 403."
    ),
)
def admin_panel_check(
    _admin: User = Depends(get_current_admin),
    _credentials=Depends(_security),
) -> dict:
    return {"message": "Admin panel accessible."}


# ──────────────────────────────────────────────────────────────────────────────
# US-17  –  View reports
# ──────────────────────────────────────────────────────────────────────────────

@router.get(
    "/reports",
    response_model=PaginatedAdminReports,
    summary="List all reports (admin)",
    description=(
        "Paginated, optionally filtered list of all community reports. "
        "'Under Review' entries are surfaced first, then newest first. "
        "Filter by status with ?status=under_review|verified_scam|safe."
    ),
)
def list_reports(
    page: int = Query(default=1, ge=1, description="Page number (1-based)"),
    limit: int = Query(default=10, ge=1, le=100, description="Rows per page"),
    status_filter: Optional[ReportStatus] = Query(
        default=None,
        alias="status",
        description="Filter by report status.",
    ),
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
    _credentials=Depends(_security),
) -> PaginatedAdminReports:
    return admin_service.get_paginated_reports(
        db=db,
        page=page,
        limit=limit,
        status_filter=status_filter,
    )


# ──────────────────────────────────────────────────────────────────────────────
# US-17  –  Update report status
# ──────────────────────────────────────────────────────────────────────────────

@router.patch(
    "/reports/{report_id}/status",
    response_model=UpdateReportStatusResponse,
    summary="Update report status (admin)",
    description=(
        "Transition a report from 'under_review' to either 'verified_scam' or "
        "'safe'. Any other transition is rejected with 400. "
        "An audit log entry is written automatically."
    ),
)
def update_report_status(
    report_id: int,
    body: UpdateReportStatusRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
    _credentials=Depends(_security),
) -> UpdateReportStatusResponse:
    return admin_service.update_report_status(
        db=db,
        report_id=report_id,
        new_status=body.new_status,
        admin_id=admin.id,
        admin_notes=body.admin_notes,
    )


# ──────────────────────────────────────────────────────────────────────────────
# US-18  –  Admin blacklist entry
# ──────────────────────────────────────────────────────────────────────────────

@router.post(
    "/reports",
    response_model=AdminAddReportResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add report to blacklist (admin)",
    description=(
        "Admin manually creates a report entry that is immediately usable by "
        "the scan / lookup layer. Duplicates (same input_type + input_value) "
        "are rejected with 400. threat_category must be 'verified_scam' or "
        "'safe'."
    ),
)
def admin_add_report(
    body: AdminAddReportRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
    _credentials=Depends(_security),
) -> AdminAddReportResponse:
    report = admin_service.admin_add_report(
        db=db,
        admin_id=admin.id,
        input_type=body.input_type,
        input_value=body.input_value,
        threat_category=body.threat_category,
        admin_notes=body.admin_notes,
    )
    return AdminAddReportResponse.model_validate(report)


# ──────────────────────────────────────────────────────────────────────────────
# US-19  –  System metrics
# ──────────────────────────────────────────────────────────────────────────────

@router.get(
    "/metrics",
    response_model=SystemMetricsResponse,
    summary="System activity metrics (admin)",
    description=(
        "Returns aggregate counts of scans and reports derived directly from "
        "the database. No values are hardcoded."
    ),
)
def system_metrics(
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
    _credentials=Depends(_security),
) -> SystemMetricsResponse:
    return admin_service.get_system_metrics(db=db)


@router.post(
    "/seed-blacklist",
    summary="Seed blacklist from file (admin)",
        description=(
            "Seeds the blacklist with entries from a CSV file. The file should have "
            "a header row and a column named 'domain' containing the domains to add."
        ),
)
def seed_blacklist_from_file(
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
    _credentials=Depends(_security),
) -> dict:
    admin_service.seed_blacklist(db=db)
    return {"message": "Blacklist seeded from file."}