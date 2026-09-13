from sqlalchemy.orm import Session
from app.models.monitored_logs_model import MonitoredLogs

class LogsRepository:

    def add_log(db: Session, log:MonitoredLogs):
        db.add(log)

    def get_logs_of_api(db: Session, api_id: str):
        return db.query(MonitoredLogs).filter(MonitoredLogs.api_id == api_id).order_by(MonitoredLogs.checked_at.desc()).all()

    def get_recent_logof_api(db: Session, api_id: str):
        return db.query(MonitoredLogs).filter(MonitoredLogs.api_id == api_id).order_by(MonitoredLogs.checked_at.desc()).first()