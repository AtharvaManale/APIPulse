from sqlalchemy.orm import Session
from app.models.apis_model import API
from app.models.monitored_logs_model import MonitoredLogs
from app.models.alerts_model import Alerts
from app.repositories.alerts_repository import AlertsRepository
from app.repositories.users_repository import UsersRepository
from app.tasks.email_tasks import send_downtime_alert_email


class AlertsService:

    @staticmethod
    def evaluate_probe(db: Session, api: API, latest_log: MonitoredLogs):

        try:
            if latest_log.is_success:
                active_alert = AlertsRepository.get_active_alert(db, api.id)
                if active_alert:
                    AlertsRepository.resolve_active_alerts(db, api.id)
                    db.commit()
                return

            recent_logs = AlertsRepository.get_recent_logs(db, api.id, limit=3)
            consecutive_failures = len(recent_logs) >= 3 and all(not l.is_success for l in recent_logs)

            if not consecutive_failures:
                return

            existing_active_alert = AlertsRepository.get_active_alert(db, api.id)
            if existing_active_alert:
                return

            last_error = latest_log.error_message or (f"HTTP {latest_log.status_code}" if latest_log.status_code else "Health check failed")
            new_alert = Alerts(
                api_id=api.id,
                type="API_DOWN",
                message=f"Endpoint failed 3 consecutive health checks. Last error: {last_error}",
                resolved=False
            )
            AlertsRepository.add_alert(db, new_alert)

            api.is_active = False
            db.commit()
            db.refresh(api)

            try:
                owner = api.user or UsersRepository.get_user_by_id(db, api.user_id)
                if owner and owner.email_id:
                    send_downtime_alert_email.delay(
                        to_email=owner.email_id,
                        username=owner.username,
                        api_name=api.api_name,
                        api_url=api.url,
                        last_error=last_error,
                        downtime_time=str(latest_log.checked_at)
                    )
            except Exception:
                pass

        except Exception:
            db.rollback()
