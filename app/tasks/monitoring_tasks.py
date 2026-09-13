from app.dependencies.celery_dependency import celery
from app.services.automations_service import AutomationService


@celery.task(name="app.tasks.monitoring_tasks.monitor_api")
def monitor_api(api_id: str, user_id: str):

    return AutomationService.execute_api_monitor(api_id=api_id, user_id=user_id)

@celery.task(name="app.tasks.monitoring_tasks.monitor_apis_by_interval")
def monitor_apis_by_interval(interval: int):

    return AutomationService.schedule_monitoring_for_interval(interval)