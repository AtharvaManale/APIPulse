from app.db.session import SessionLocal
from app.repositories.apis_repository import ApiRepository
from app.services.monitoring_service import MonitoringService


class AutomationService:

    @staticmethod
    def schedule_monitoring_for_interval(interval: int):

        from app.tasks.monitoring_tasks import monitor_api

        db = SessionLocal()
        try:
            active_apis = ApiRepository.get_active_apis_by_interval(db, interval)

            for api in active_apis:
                monitor_api.delay(api_id=api.id, user_id=api.user_id)

            return len(active_apis)
        except Exception as e:
            raise
        finally:
            db.close()

    @staticmethod
    def execute_api_monitor(api_id: str, user_id: str):

        db = SessionLocal()
        try:
            log = MonitoringService.monitor_api_endpoint(db, api_id=api_id, user_id=user_id)

            return {
                "api_id": log.api_id,
                "status_code": log.status_code,
                "latency_ms": log.latency_ms,
                "is_success": log.is_success,
                "checked_at": str(log.checked_at),
            }
        except Exception as e:
            raise
        finally:
            db.close()
