"""
routers/scan.py
---------------
Scan (threat detection) endpoints.

Routes:
  POST /scan/url      analyze a URL
  POST /scan/text     analyze a text message
  POST /scan/phone    analyze a phone number
  GET  /scan/history  paginated scan history for current user
"""

from fastapi import APIRouter, Depends, Query
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database import get_db
from app.schemas.scan import (
    ScanHistoryResponse,
    ScanPhoneRequest,
    ScanResult,
    ScanTextRequest,
    ScanURLRequest,
)
from app.services import scan_service

router = APIRouter(prefix="/scan", tags=["Scan"])
_security = HTTPBearer()


# ──────────────────────────────────────────────
# POST /scan/url
# ──────────────────────────────────────────────

@router.post(
    "/url",
    response_model=ScanResult,
    summary="Analyze a URL",
    description=(
        "Validates the URL format then checks the reputation database "
        "and community reports to produce a final threat category."
    ),
)
def scan_url(
    request: ScanURLRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _credentials=Depends(_security),
) -> ScanResult:
    result = scan_service.analyze_url(
        db=db,
        user_id=current_user.id,
        url=request.url,
    )
    return ScanResult(**result)


# ──────────────────────────────────────────────
# POST /scan/text
# ──────────────────────────────────────────────

@router.post(
    "/text",
    response_model=ScanResult,
    summary="Analyze a text message",
    description=(
        "Runs the ML classifier on the message (translating Arabic automatically), "
        "extracts and analyzes any embedded URLs, and optionally incorporates "
        "the sender phone number's risk profile."
    ),
)
def scan_text(
    request: ScanTextRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _credentials=Depends(_security),
) -> ScanResult:
    result = scan_service.analyze_text(
        db=db,
        user_id=current_user.id,
        message=request.message,
        phone_number=request.phone_number,
    )
    return ScanResult(**result)


# ──────────────────────────────────────────────
# POST /scan/phone
# ──────────────────────────────────────────────

@router.post(
    "/phone",
    response_model=ScanResult,
    summary="Analyze a phone number",
    description=(
        "Looks up the phone number in aggregated community report data "
        "and returns a risk category. Returns 'no_data' if the number "
        "has never been reported."
    ),
)
def scan_phone(
    request: ScanPhoneRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _credentials=Depends(_security),
) -> ScanResult:
    result = scan_service.analyze_phone(
        db=db,
        user_id=current_user.id,
        phone_number=request.phone_number,
    )
    return ScanResult(**result)


# ──────────────────────────────────────────────
# GET /scan/history
# ──────────────────────────────────────────────

@router.get(
    "/history",
    response_model=ScanHistoryResponse,
    summary="Paginated scan history",
    description=(
        "Returns the authenticated user's scan history ordered by most recent first. "
        "page_size is capped at 50."
    ),
)
def scan_history(
    page: int = Query(default=1, ge=1, description="Page number (1-based)"),
    page_size: int = Query(default=10, ge=1, le=50, description="Items per page (max 50)"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _credentials=Depends(_security),
) -> ScanHistoryResponse:
    data = scan_service.get_user_scan_history(
        db=db,
        user_id=current_user.id,
        page=page,
        page_size=page_size,
    )
    return ScanHistoryResponse(**data)
