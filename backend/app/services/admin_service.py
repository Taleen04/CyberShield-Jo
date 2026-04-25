"""
services/admin_service.py
--------------------------
Business logic for admin-only operations.

Implements
----------
  get_paginated_reports()        US-17  list / filter / sort reports
  update_report_status()         US-17  status transition + audit log
  admin_add_report()             US-18  admin blacklist entry
  get_system_metrics()           US-19  aggregate counts
  _write_audit_log()             internal helper
"""

from __future__ import annotations

import csv
import logging
import math
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING, Optional

from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from tld import get_tld

from app.models.admin_audit_log import AdminAuditLog
from app.models.lookup import InputType, ReportStatus, ThreatCategory
from app.models.scan import Scan, PhoneNumber, Report
from app.schemas.admin import (
    AdminReportListItem,
    DailyCount,
    PaginatedAdminReports,
    PaginationMeta,
    PhoneMetrics,
    ReportMetrics,
    ReportOriginBreakdown,
    ReportStatusBreakdown,
    ScanBreakdown,
    ScanMetrics,
    SystemMetricsResponse,
    ThreatBreakdown,
    TopThreatEntry,
    UpdateReportStatusResponse,
)

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────────────────────

# Only reports currently "under_review" may be transitioned by an admin.
_ALLOWED_TRANSITIONS: dict[ReportStatus, set[ReportStatus]] = {
    ReportStatus.UNDER_REVIEW: {ReportStatus.VERIFIED_SCAM, ReportStatus.SAFE},
}


# ──────────────────────────────────────────────────────────────────────────────
# US-17  –  View & manage reports
# ──────────────────────────────────────────────────────────────────────────────

def get_paginated_reports(
    db: Session,
    page: int,
    limit: int,
    status_filter: Optional[ReportStatus],
) -> PaginatedAdminReports:
    """
    Return a paginated, optionally-filtered list of all reports.

    Sorting guarantee
    -----------------
    • UNDER_REVIEW reports appear first (priority 0).
    • All other statuses follow (priority 1), then by created_at DESC.

    Parameters
    ----------
    db            : active SQLAlchemy session
    page          : 1-based page number
    limit         : rows per page (1–100)
    status_filter : when provided, only rows matching this status are returned
    """
    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Page number must be 1 or greater.",
        )
    if not (1 <= limit <= 100):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limit must be between 1 and 100.",
        )

    query = db.query(Report)

    if status_filter is not None:
        query = query.filter(Report.status == status_filter)

    # Sort: UNDER_REVIEW first, then by newest submission.
    priority_expr = (
        (Report.status != ReportStatus.UNDER_REVIEW).cast(db.bind.dialect.name == "postgresql" and "int" or "integer")
        if False  # placeholder – replaced below with portable expression
        else func.case(
            (Report.status == ReportStatus.UNDER_REVIEW, 0),
            else_=1,
        )
    )
    query = query.order_by(priority_expr, Report.created_at.desc())

    total = query.count()
    total_pages = max(1, math.ceil(total / limit))
    offset = (page - 1) * limit

    rows = query.offset(offset).limit(limit).all()

    return PaginatedAdminReports(
        items=[AdminReportListItem.model_validate(r) for r in rows],
        meta=PaginationMeta(
            page=page,
            limit=limit,
            total=total,
            total_pages=total_pages,
        ),
    )


def update_report_status(
    db: Session,
    report_id: int,
    new_status: ReportStatus,
    admin_id: int,
    admin_notes: Optional[str],
) -> UpdateReportStatusResponse:
    """
    Transition a report's status and persist an audit log entry.

    Allowed transitions
    -------------------
    UNDER_REVIEW → VERIFIED_SCAM | SAFE

    Raises
    ------
    404  if the report does not exist
    400  if the transition is not permitted
    """
    report = db.query(Report).filter(Report.id == report_id).first()
    if report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report {report_id} not found.",
        )

    old_status: ReportStatus = report.status
    _validate_transition(old_status, new_status, report_id)

    # Apply changes
    report.status = new_status
    report.reviewed_by_admin_id = admin_id
    report.reviewed_at = datetime.now(timezone.utc)
    if admin_notes is not None:
        report.admin_notes = admin_notes

    # Persist audit log before committing the main change so both land in one
    # transaction and neither can succeed without the other.
    _write_audit_log(
        db=db,
        admin_id=admin_id,
        report_id=report_id,
        old_status=old_status,
        new_status=new_status,
        notes=admin_notes,
        flush_only=True,  # commit happens once below
    )

    db.commit()
    db.refresh(report)

    logger.info(
        "Admin %d changed report %d status: %s → %s",
        admin_id,
        report_id,
        old_status.value,
        new_status.value,
    )

    return UpdateReportStatusResponse(
        id=report.id,
        old_status=old_status,
        new_status=report.status,
        reviewed_by_admin_id=admin_id,
        reviewed_at=report.reviewed_at,
        admin_notes=report.admin_notes,
    )


# ──────────────────────────────────────────────────────────────────────────────
# US-18  –  Admin blacklist entry
# ──────────────────────────────────────────────────────────────────────────────

def admin_add_report(
    db: Session,
    admin_id: int,
    input_type: InputType,
    input_value: str,
    threat_category: ReportStatus,
    admin_notes: Optional[str],
) -> Report:
    """
    Admin manually inserts a report entry into the system.

    Rules
    -----
    • Duplicates (same input_value + input_type) are rejected with 400.
    • threat_category must be VERIFIED_SCAM or SAFE (not UNDER_REVIEW).
    • admin_added is set to True so downstream scan logic can identify origin.
    • The record is immediately usable by the scan / lookup layer.

    Parameters
    ----------
    db              : active SQLAlchemy session
    admin_id        : id of the authenticated admin (used as user_id)
    input_type      : URL | PHONE | TEXT_MESSAGE
    input_value     : the actual value being blacklisted
    threat_category : final verdict – VERIFIED_SCAM or SAFE
    admin_notes     : optional contextual note
    """
    if threat_category == ReportStatus.UNDER_REVIEW:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "threat_category cannot be 'under_review' for admin-added entries. "
                "Use 'verified_scam' or 'safe'."
            ),
        )

    _assert_no_duplicate(db, input_type, input_value)

    report = Report(
        user_id=admin_id,
        input_type=input_type,
        input_value=input_value,
        status=threat_category,
        admin_added=True,
        admin_notes=admin_notes,
        reviewed_by_admin_id=admin_id,
        reviewed_at=datetime.now(timezone.utc),
    )
    db.add(report)
    db.commit()
    db.refresh(report)

    logger.info(
        "Admin %d added blacklist entry: type=%s value=%r status=%s",
        admin_id,
        input_type.value,
        input_value,
        threat_category.value,
    )

    return report


# ──────────────────────────────────────────────────────────────────────────────
# US-19  –  System metrics
# ──────────────────────────────────────────────────────────────────────────────

def get_system_metrics(db: Session) -> SystemMetricsResponse:
    """
    Build a comprehensive system-activity dashboard payload.

    Sections
    --------
    scans
        • total / today / 7-day / 30-day counts
        • breakdown by input_type and threat_category
        • average ML confidence score
        • per-day counts for the last 7 calendar days

    reports
        • total / today / 7-day / 30-day counts
        • pending-review count
        • breakdown by status, input_type, and origin (user vs admin)
        • per-day counts for the last 7 calendar days

    phone_numbers
        • total tracked numbers
        • average spam rate

    top_threats
        • top-10 most-reported input values (by report count)

    All counts are derived directly from database queries — nothing is hardcoded.
    """
    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    last_7_start = today_start - timedelta(days=6)   # inclusive of today → 7 days
    last_30_start = today_start - timedelta(days=29)

    return SystemMetricsResponse(
        generated_at=now,
        scans=_build_scan_metrics(db, today_start, last_7_start, last_30_start),
        reports=_build_report_metrics(db, today_start, last_7_start, last_30_start),
        phone_numbers=_build_phone_metrics(db),
        top_threats=_build_top_threats(db, limit=10),
    )


# ── metrics helpers ────────────────────────────────────────────────────────────

def _build_scan_metrics(
    db: Session,
    today_start: datetime,
    last_7_start: datetime,
    last_30_start: datetime,
) -> "ScanMetrics":
    """Derive all scan-related metrics from the scans table."""

    total: int = db.query(func.count(Scan.id)).scalar() or 0
    today: int = (
        db.query(func.count(Scan.id))
        .filter(Scan.created_at >= today_start)
        .scalar() or 0
    )
    last_7: int = (
        db.query(func.count(Scan.id))
        .filter(Scan.created_at >= last_7_start)
        .scalar() or 0
    )
    last_30: int = (
        db.query(func.count(Scan.id))
        .filter(Scan.created_at >= last_30_start)
        .scalar() or 0
    )

    # --- by_input_type ---
    type_rows = (
        db.query(Scan.input_type, func.count(Scan.id))
        .group_by(Scan.input_type)
        .all()
    )
    by_input_type = ScanBreakdown(
        **{row.input_type.value: row[1] for row in type_rows}
    )

    # --- by_threat_category ---
    threat_rows = (
        db.query(Scan.threat_category, func.count(Scan.id))
        .group_by(Scan.threat_category)
        .all()
    )
    by_threat = ThreatBreakdown(
        **{row.threat_category.value: row[1] for row in threat_rows}
    )

    # --- average ML confidence (only scans that have a score) ---
    avg_confidence: Optional[float] = (
        db.query(func.avg(Scan.ml_confidence))
        .filter(Scan.ml_confidence.isnot(None))
        .scalar()
    )
    if avg_confidence is not None:
        avg_confidence = round(float(avg_confidence), 2)

    # --- daily counts for the last 7 calendar days ---
    daily_scans = _daily_counts(
        db=db,
        model=Scan,
        date_col=Scan.created_at,
        since=last_7_start,
    )

    return ScanMetrics(
        total=total,
        today=today,
        last_7_days=last_7,
        last_30_days=last_30,
        by_input_type=by_input_type,
        by_threat_category=by_threat,
        average_ml_confidence=avg_confidence,
        daily_last_7_days=daily_scans,
    )


def _build_report_metrics(
    db: Session,
    today_start: datetime,
    last_7_start: datetime,
    last_30_start: datetime,
) -> "ReportMetrics":
    """Derive all report-related metrics from the reports table."""

    total: int = db.query(func.count(Report.id)).scalar() or 0
    today: int = (
        db.query(func.count(Report.id))
        .filter(Report.created_at >= today_start)
        .scalar() or 0
    )
    last_7: int = (
        db.query(func.count(Report.id))
        .filter(Report.created_at >= last_7_start)
        .scalar() or 0
    )
    last_30: int = (
        db.query(func.count(Report.id))
        .filter(Report.created_at >= last_30_start)
        .scalar() or 0
    )
    pending: int = (
        db.query(func.count(Report.id))
        .filter(Report.status == ReportStatus.UNDER_REVIEW)
        .scalar() or 0
    )

    # --- by_status ---
    status_rows = (
        db.query(Report.status, func.count(Report.id))
        .group_by(Report.status)
        .all()
    )
    by_status = ReportStatusBreakdown(
        **{row.status.value: row[1] for row in status_rows}
    )

    # --- by_input_type (same ScanBreakdown shape) ---
    rtype_rows = (
        db.query(Report.input_type, func.count(Report.id))
        .group_by(Report.input_type)
        .all()
    )
    by_input_type = ScanBreakdown(
        **{row.input_type.value: row[1] for row in rtype_rows}
    )

    # --- by_origin ---
    admin_count: int = (
        db.query(func.count(Report.id))
        .filter(Report.admin_added.is_(True))
        .scalar() or 0
    )
    by_origin = ReportOriginBreakdown(
        admin_added=admin_count,
        user_submitted=total - admin_count,
    )

    # --- daily counts for the last 7 calendar days ---
    daily_reports = _daily_counts(
        db=db,
        model=Report,
        date_col=Report.created_at,
        since=last_7_start,
    )

    return ReportMetrics(
        total=total,
        today=today,
        last_7_days=last_7,
        last_30_days=last_30,
        pending_review=pending,
        by_status=by_status,
        by_input_type=by_input_type,
        by_origin=by_origin,
        daily_last_7_days=daily_reports,
    )


def _build_phone_metrics(db: Session) -> "PhoneMetrics":
    """Derive summary stats from the phone_numbers table."""

    total_tracked: int = db.query(func.count(PhoneNumber.id)).scalar() or 0

    avg_spam_raw = (
        db.query(func.avg(PhoneNumber.spam_reports / func.nullif(PhoneNumber.total_reports, 0)))
        .filter(PhoneNumber.total_reports > 0)
        .scalar()
    )
    avg_spam: Optional[float] = (
        round(float(avg_spam_raw), 4) if avg_spam_raw is not None else None
    )

    return PhoneMetrics(
        total_tracked=total_tracked,
        average_spam_rate=avg_spam,
    )


def _build_top_threats(db: Session, limit: int = 10) -> list["TopThreatEntry"]:
    """
    Return the top N most-reported input values across all report types.

    Groups by (input_type, input_value) and orders by descending report count.
    """
    rows = (
        db.query(
            Report.input_type,
            Report.input_value,
            func.count(Report.id).label("report_count"),
        )
        .group_by(Report.input_type, Report.input_value)
        .order_by(func.count(Report.id).desc())
        .limit(limit)
        .all()
    )
    return [
        TopThreatEntry(
            input_type=row.input_type,
            input_value=row.input_value,
            report_count=row.report_count,
        )
        for row in rows
    ]


def _daily_counts(
    db: Session,
    model,
    date_col,
    since: datetime,
) -> list["DailyCount"]:
    """
    Return per-day row counts from *since* up to and including today.

    Uses a Python-side aggregation pass so the query stays database-agnostic
    (SQLite's strftime vs PostgreSQL's date_trunc both work transparently via
    the ORM datetime column).

    Parameters
    ----------
    db       : active session
    model    : the SQLAlchemy model class (Scan or Report)
    date_col : the DateTime column to bucket on
    since    : inclusive lower bound (UTC midnight of the earliest date)
    """
    rows = (
        db.query(date_col)
        .filter(date_col >= since)
        .all()
    )

    # Bucket into calendar dates (UTC)
    counts: dict[str, int] = {}
    for (dt,) in rows:
        day = dt.strftime("%Y-%m-%d")
        counts[day] = counts.get(day, 0) + 1

    # Fill every day in the window so the frontend always gets a dense series
    result: list[DailyCount] = []
    now_utc = datetime.now(timezone.utc)
    cursor = since
    while cursor <= now_utc:
        day = cursor.strftime("%Y-%m-%d")
        result.append(DailyCount(date=day, count=counts.get(day, 0)))
        cursor += timedelta(days=1)

    return result


# ──────────────────────────────────────────────────────────────────────────────
# Private helpers
# ──────────────────────────────────────────────────────────────────────────────

def _validate_transition(
    old_status: ReportStatus,
    new_status: ReportStatus,
    report_id: int,
) -> None:
    """
    Raise 400 if the requested status transition is not permitted.

    Parameters
    ----------
    old_status : current status of the report
    new_status : desired target status
    report_id  : used only for the error message
    """
    allowed = _ALLOWED_TRANSITIONS.get(old_status, set())
    if new_status not in allowed:
        allowed_labels = ", ".join(s.value for s in allowed) or "none"
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Cannot transition report {report_id} from '{old_status.value}' "
                f"to '{new_status.value}'. "
                f"Allowed target(s) from this state: [{allowed_labels}]."
            ),
        )


def _assert_no_duplicate(
    db: Session,
    input_type: InputType,
    input_value: str,
) -> None:
    """
    Raise 400 if a report with the same (input_type, input_value) already exists.

    Parameters
    ----------
    db          : active SQLAlchemy session
    input_type  : type of the input being checked
    input_value : value of the input being checked
    """
    existing = (
        db.query(Report)
        .filter(
            Report.input_type == input_type,
            Report.input_value == input_value,
        )
        .first()
    )
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"A report for input_type='{input_type.value}' with this "
                f"input_value already exists (report id={existing.id})."
            ),
        )


def _write_audit_log(
    db: Session,
    admin_id: int,
    report_id: int,
    old_status: ReportStatus,
    new_status: ReportStatus,
    notes: Optional[str],
    *,
    flush_only: bool = False,
) -> AdminAuditLog:
    """
    Persist an audit log row for a status change.

    Parameters
    ----------
    db          : active SQLAlchemy session
    admin_id    : id of the admin performing the action
    report_id   : id of the affected report
    old_status  : status before the change
    new_status  : status after the change
    notes       : optional admin note (may be None)
    flush_only  : when True, only flush to session (caller commits); when False,
                  this function commits itself (standalone use).
    """
    entry = AdminAuditLog(
        admin_id=admin_id,
        report_id=report_id,
        old_status=old_status,
        new_status=new_status,
        notes=notes,
        timestamp=datetime.now(timezone.utc),
    )
    db.add(entry)

    if flush_only:
        db.flush()
    else:
        db.commit()
        db.refresh(entry)

    return entry


def _process_tld(url):
    try:
        res = get_tld(url, as_object=True, fix_protocol=True)
        return res.parsed_url.netloc
    except:
        return None


def _load_blacklist_domains(file_path: str) -> list[str]:
    domains = []

    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)

        for row in reader:
            if not row:
                continue

            domain = _process_tld(row[0])

            if domain:
                domains.append(domain)

    return list(set(domains))  # deduplicate


def seed_blacklist(db: Session, file_path = "app/ml/datasets/archive/phish_blacklist.csv"):
    domains = _load_blacklist_domains(file_path)
    for domain in domains:
        print(f"[seed] seeding url: {domain}")
        admin_add_report(
            db=db,
            admin_id=19,  # system user
            input_type=InputType.URL,
            input_value=domain,
            threat_category=ReportStatus.VERIFIED_SCAM,
            admin_notes="Seeded from phishtank dataset"
        )