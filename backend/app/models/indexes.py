from app.models.scan import Scan
from backend.app.models.auth import UserSession
from app.models.scan import Report

from sqlalchemy import Index

# Index for finding scans by user and date
Index('idx_scans_user_created', Scan.user_id, Scan.created_at.desc())

# Index for finding reports by user and status
Index('idx_reports_user_status', Report.user_id, Report.status)

# Index for active sessions
Index('idx_sessions_expires', UserSession.expires_at)