"""
models/admin_audit_log.py
--------------------------
Persistent audit trail for every admin action that changes a report's status.
"""

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.lookup import ReportStatus


class AdminAuditLog(Base):
    """
    Records every status transition performed by an admin.

    Fields
    ------
    id              : surrogate PK
    admin_id        : FK → users.id  (the admin who made the change)
    report_id       : FK → reports.id
    old_status      : status value before the change
    new_status      : status value after the change
    timestamp       : UTC moment the change was committed
    notes           : optional free-text note captured at change time
    """

    __tablename__ = "admin_audit_logs"

    id = Column(Integer, primary_key=True, index=True)

    admin_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    report_id = Column(
        Integer,
        ForeignKey("reports.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    old_status = Column(SQLEnum(ReportStatus, name="report_status"), nullable=False)
    new_status = Column(SQLEnum(ReportStatus, name="report_status"), nullable=False)

    timestamp = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )
    notes = Column(Text, nullable=True)

    # Relationships (read-only convenience; no cascades required here)
    admin = relationship("User", foreign_keys=[admin_id])
    report = relationship("Report", foreign_keys=[report_id])
