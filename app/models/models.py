from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base


class PhoneNumber(Base):
    """
    Tracks a phone number that has been reported at least once.
    Central table — everything links back here.
    """
    __tablename__ = "phone_numbers"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String(20), unique=True, index=True, nullable=False)
    total_reports = Column(Integer, default=0)
    spam_reports = Column(Integer, default=0)
    ham_reports = Column(Integer, default=0)

    first_seen = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    last_seen = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    predictions = relationship("PredictionLog", back_populates="phone")

    @property
    def spam_rate(self) -> float:
        if self.total_reports == 0:
            return 0.0
        return round(self.spam_reports / self.total_reports, 4)


class PredictionLog(Base):
    """
    Logs every single prediction request made by the API.
    """
    __tablename__ = "prediction_logs"

    id = Column(Integer, primary_key=True, index=True)
    phone_number_id = Column(Integer, ForeignKey("phone_numbers.id"), nullable=True)

    message_text = Column(Text, nullable=False)
    predicted_label = Column(String(10), nullable=False)  # "spam" or "ham"
    confidence = Column(Float, nullable=False)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    phone = relationship("PhoneNumber", back_populates="predictions")