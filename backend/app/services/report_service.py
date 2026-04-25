"""
report_service.py
-----------------
All business logic for user-submitted community reports.

Implements:
  - create_report_from_scan()
  - create_manual_report()
  - get_user_reports()
"""

from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.lookup import InputType, ReportStatus
from app.models.scan import Report
from app.models.scan import Scan


def create_report_from_scan(
    db: Session,
    user_id: int,
    scan_id: int,
    notes: Optional[str],
) -> Report:
    """
    Create a report pre-filled from an existing scan.

    - input_type and input_value are copied from the scan (not modifiable).
    - analysis_result is copied verbatim from the scan's analysis_details.
    - status is initialised to UNDER_REVIEW.

    Raises 404 if the scan does not exist or does not belong to the user.
    """
    scan = (
        db.query(Scan)
        .filter(Scan.id == scan_id, Scan.user_id == user_id)
        .first()
    )
    if scan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scan not found or does not belong to the current user.",
        )

    report = Report(
        user_id=user_id,
        input_type=scan.input_type,
        input_value=scan.input_value,
        notes=notes,
        scan_id=scan_id,
        analysis_result=scan.analysis_details,
        status=ReportStatus.UNDER_REVIEW,
        admin_added = False
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


def create_manual_report(
    db: Session,
    user_id: int,
    input_type: InputType,
    input_value: str,
    location_inside_jordan: bool,
    notes: Optional[str],
) -> Report:
    """
    Create a report without a prior analysis (manual submission).

    - location_inside_jordan is required for manual reports (US-11-B).
    - status is initialised to UNDER_REVIEW.
    - No analysis_result is attached.
    """
    report = Report(
        user_id=user_id,
        input_type=input_type,
        input_value=input_value,
        notes=notes,
        location_inside_jordan=location_inside_jordan,
        status=ReportStatus.UNDER_REVIEW,
        admin_added = False
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


def get_user_reports(db: Session, user_id: int) -> list[Report]:
    """
    Return all reports submitted by the given user, newest first.
    """
    return (
        db.query(Report)
        .filter(Report.user_id == user_id)
        .order_by(Report.created_at.desc())
        .all()
    )
