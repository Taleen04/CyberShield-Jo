"""
routers/report.py
-----------------
Community reporting endpoints.

Routes:
  POST /report/from-scan    report based on an existing scan
  POST /report/manual       manual report without prior analysis
  GET  /report/my-reports   list reports submitted by the current user
"""
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database import get_db
from app.schemas.report import ManualReportRequest, MyReportItem, ReportFromScanRequest, ReportResponse
from app.services import report_service

router = APIRouter(prefix="/report", tags=["Report"])
_security = HTTPBearer()


# ──────────────────────────────────────────────
# POST /report/from-scan
# ──────────────────────────────────────────────

@router.post(
    "/from-scan",
    response_model=ReportResponse,
    status_code=201,
    summary="Report after analysis",
    description=(
        "Submit a report linked to a previously completed scan. "
        "input_type and input_value are read directly from the scan and "
        "cannot be overridden. An optional free-text note may be added."
    ),
)
def report_from_scan(
    request: ReportFromScanRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _credentials=Depends(_security),
) -> ReportResponse:
    report = report_service.create_report_from_scan(
        db=db,
        user_id=current_user.id,
        scan_id=request.scan_id,
        notes=request.notes,
    )
    return ReportResponse.model_validate(report)


# ──────────────────────────────────────────────
# POST /report/manual
# ──────────────────────────────────────────────

@router.post(
    "/manual",
    response_model=ReportResponse,
    status_code=201,
    summary="Manual report (no analysis)",
    description=(
        "Submit a report without performing an analysis first. "
        "input_type, input_value, and location_inside_jordan are required. "
        "Only submit inputs you know or suspect are malicious."
    ),
)
def report_manual(
    request: ManualReportRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _credentials=Depends(_security),
) -> ReportResponse:
    report = report_service.create_manual_report(
        db=db,
        user_id=current_user.id,
        input_type=request.input_type,
        input_value=request.input_value,
        location_inside_jordan=request.location_inside_jordan,
        notes=request.notes,
    )
    return ReportResponse.model_validate(report)


# ──────────────────────────────────────────────
# GET /report/my-reports
# ──────────────────────────────────────────────

@router.get(
    "/my-reports",
    response_model=list[MyReportItem],
    summary="My submitted reports",
    description=(
        "Returns all reports submitted by the authenticated user, "
        "ordered by submission date (newest first). "
        "Each entry shows the reported item, input type, date, and current status."
    ),
)
def my_reports(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _credentials=Depends(_security),
) -> list[MyReportItem]:
    reports = report_service.get_user_reports(db=db, user_id=current_user.id)
    return [MyReportItem.model_validate(r) for r in reports]
