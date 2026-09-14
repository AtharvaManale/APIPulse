import smtplib
from app.dependencies.celery_dependency import celery
from app.services.email_service import EmailService


@celery.task(
    bind=True,
    name="app.tasks.email_tasks.send_downtime_alert_email",
    max_retries=3,
    default_retry_delay=60
)
def send_downtime_alert_email(
    self,
    to_email: str,
    username: str,
    api_name: str,
    api_url: str,
    last_error: str,
    downtime_time: str | None = None
):
    try:
        return EmailService.send_downtime_alert(
            to_email=to_email,
            username=username,
            api_name=api_name,
            api_url=api_url,
            last_error=last_error,
            downtime_time=downtime_time
        )
    except smtplib.SMTPException as exc:
        raise self.retry(exc=exc, countdown=60)
