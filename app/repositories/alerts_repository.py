from datetime import datetime
from sqlalchemy.orm import Session
from app.models.alerts_model import Alerts
from app.models.monitored_logs_model import MonitoredLogs


class AlertsRepository:

    @staticmethod
    def get_active_alert(db: Session, api_id: str) -> Alerts | None:
        return (
            db.query(Alerts)
            .filter(Alerts.api_id == api_id, Alerts.resolved == False)
            .first()
        )

    @staticmethod
    def add_alert(db: Session, alert: Alerts):
        db.add(alert)

    @staticmethod
    def get_recent_logs(db: Session, api_id: str, limit: int = 3) -> list[MonitoredLogs]:
        return (
            db.query(MonitoredLogs)
            .filter(MonitoredLogs.api_id == api_id)
            .order_by(MonitoredLogs.checked_at.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def resolve_active_alerts(db: Session, api_id: str):
        active_alerts = (
            db.query(Alerts)
            .filter(Alerts.api_id == api_id, Alerts.resolved == False)
            .all()
        )
        now = datetime.now()
        for alert in active_alerts:
            alert.resolved = True
            alert.resolved_at = now
