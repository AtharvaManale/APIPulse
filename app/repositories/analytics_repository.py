from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.monitored_logs_model import MonitoredLogs


class AnalyticsRepository:

    @staticmethod
    def get_latencies_in_window(db: Session, api_id: str, since: datetime) -> list[int]:
        rows = (
            db.query(MonitoredLogs.latency_ms)
            .filter(
                MonitoredLogs.api_id == api_id,
                MonitoredLogs.checked_at >= since,
                MonitoredLogs.latency_ms.isnot(None)
            )
            .order_by(MonitoredLogs.latency_ms.asc())
            .all()
        )
        return [r[0] for r in rows if r[0] is not None]

    @staticmethod
    def get_status_code_distribution(db: Session, api_id: str, since: datetime) -> dict[str, int]:
        results = (
            db.query(MonitoredLogs.status_code, func.count(MonitoredLogs.id))
            .filter(
                MonitoredLogs.api_id == api_id,
                MonitoredLogs.checked_at >= since
            )
            .group_by(MonitoredLogs.status_code)
            .all()
        )
        distribution = {}
        for code, count in results:
            key = str(code) if code is not None else "failed/timeout"
            distribution[key] = count
        return distribution

    @staticmethod
    def get_success_failure_counts(db: Session, api_id: str, since: datetime) -> tuple[int, int]:
        results = (
            db.query(MonitoredLogs.is_success, func.count(MonitoredLogs.id))
            .filter(
                MonitoredLogs.api_id == api_id,
                MonitoredLogs.checked_at >= since
            )
            .group_by(MonitoredLogs.is_success)
            .all()
        )
        success_count = 0
        failure_count = 0
        for is_success, count in results:
            if is_success:
                success_count = count
            else:
                failure_count = count
        return success_count, failure_count

    @staticmethod
    def get_latest_log(db: Session, api_id: str) -> MonitoredLogs | None:
        return (
            db.query(MonitoredLogs)
            .filter(MonitoredLogs.api_id == api_id)
            .order_by(MonitoredLogs.checked_at.desc())
            .first()
        )

    @staticmethod
    def get_trend_logs(db: Session, api_id: str, since: datetime, limit: int = 100) -> list[MonitoredLogs]:
        return (
            db.query(MonitoredLogs)
            .filter(
                MonitoredLogs.api_id == api_id,
                MonitoredLogs.checked_at >= since
            )
            .order_by(MonitoredLogs.checked_at.asc())
            .limit(limit)
            .all()
        )
