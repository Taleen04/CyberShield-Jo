from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from fastapi.security import HTTPBearer
from app.database import get_db
from app.schemas.schemas import PredictRequest, PredictResponse
from app.models.models import PredictionLog, PhoneNumber
import app.ml.classifier as classifier
from app.api.deps import get_current_user

router = APIRouter(prefix="/scan", tags=["Prediction"])
security = HTTPBearer()


@router.post("/text", response_model=PredictResponse)
def predict_text(request: PredictRequest,
                 db: Session = Depends(get_db),
                 current_user=Depends(get_current_user),
                 credentials = Depends(security)):
    # 1. Run the ML model
    result = classifier.predict(request.message, request.message_source)

    phone_record = None

    # 2. If a phone number was provided, upsert it and update counters
    if request.phone_number:
        phone_record = (
            db.query(PhoneNumber)
            .filter(PhoneNumber.number == request.phone_number)
            .first()
        )

        if not phone_record:
            # First time we've seen this number — create a new row
            phone_record = PhoneNumber(number=request.phone_number)
            db.add(phone_record)
            db.flush()  # assign an ID before we link predictions to it

        # Update counters
        phone_record.total_reports += 1
        phone_record.last_seen = datetime.now(timezone.utc)

        if result["label"] == "spam":
            phone_record.spam_reports += 1
        else:
            phone_record.ham_reports += 1

    # 3. Log the prediction
    log = PredictionLog(
        phone_number_id=phone_record.id if phone_record else None,
        message_text=request.message,
        predicted_label=result["label"],
        confidence=result["confidence"],
    )
    db.add(log)
    db.commit()
    db.refresh(log)

    return PredictResponse(
        label=result["label"],
        confidence=result["confidence"],
        phone_number=request.phone_number,
        log_id=log.id,
    )