from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.auth import User

router = APIRouter(prefix="/admin/test", tags=["testing purposes"])

@router.post("/truncate-users")
def truncate_users(db: Session = Depends(get_db)):
    """Truncate the users table - for testing purposes only!"""

    try:
        # Delete all rows
        db.query(User).delete()
        db.commit()

        return {"message": "Users table cleared and IDs reset."}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))