from app.dependencies.celery_dependency import celery
from app.services.email_service import EmailService


@celery.task(name="app.tasks.email_tasks.send_downtime_alert_email")
def send_downtime_alert_email(
    to_email: str,
    username: str,
    api_name: str,
    api_url: str,
    last_error: str,
    downtime_time: str | None = None
):
    return EmailService.send_downtime_alert(
        to_email=to_email,
        username=username,
        api_name=api_name,
        api_url=api_url,
        last_error=last_error,
        downtime_time=downtime_time
    )
