from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import PhoneNumber
from app.schemas.schemas import PhoneNumberSummary, PhoneNumberDetail

router = APIRouter(prefix="/admin/reports", tags=["Admin Reports"])


@router.get("/", response_model=list[PhoneNumberSummary])
def list_reported_numbers(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    spam_only: bool = Query(False, description="Only return numbers with at least 1 spam report"),
    db: Session = Depends(get_db),
):
    """Returns all tracked phone numbers, paginated."""
    query = db.query(PhoneNumber)

    if spam_only:
        query = query.filter(PhoneNumber.spam_reports > 0)

    numbers = (
        query
        .order_by(PhoneNumber.spam_reports.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    # Attach the computed spam_rate property
    return [
        PhoneNumberSummary(
            id=n.id,
            number=n.number,
            total_reports=n.total_reports,
            spam_reports=n.spam_reports,
            ham_reports=n.ham_reports,
            spam_rate=n.spam_rate,
            first_seen=n.first_seen,
            last_seen=n.last_seen,
        )
        for n in numbers
    ]


@router.get("/{phone_number}", response_model=PhoneNumberDetail)
def get_phone_report(phone_number: str, db: Session = Depends(get_db)):
    """
    Returns full details for a specific phone number,
    including a list of every prediction ever made for it.
    """
    # URL-encode '+' in phone numbers will arrive as the literal string
    record = db.query(PhoneNumber).filter(PhoneNumber.number == phone_number).first()

    if not record:
        raise HTTPException(status_code=404, detail=f"Phone number '{phone_number}' not found.")

    return PhoneNumberDetail(
        id=record.id,
        number=record.number,
        total_reports=record.total_reports,
        spam_reports=record.spam_reports,
        ham_reports=record.ham_reports,
        spam_rate=record.spam_rate,
        first_seen=record.first_seen,
        last_seen=record.last_seen,
        predictions=[
            {
                "id": p.id,
                "message_text": p.message_text,
                "predicted_label": p.predicted_label,
                "confidence": p.confidence,
                "created_at": p.created_at,
            }
            for p in record.predictions
        ],
    )


@router.delete("/{phone_number}", status_code=204)
def delete_phone_record(phone_number: str, db: Session = Depends(get_db)):
    """Removes a phone number and all its associated logs."""
    record = db.query(PhoneNumber).filter(PhoneNumber.number == phone_number).first()
    if not record:
        raise HTTPException(status_code=404, detail="Phone number not found.")
    db.delete(record)
    db.commit()