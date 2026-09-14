import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from app.core.config import settings


class EmailService:

    @staticmethod
    def send_downtime_alert(
        to_email: str,
        username: str,
        api_name: str,
        api_url: str,
        last_error: str,
        downtime_time: str | None = None
    ) -> bool:
        if not downtime_time:
            downtime_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

        subject = f"🚨 [APIPulse Alert] Your API '{api_name}' is DOWN"

        plain_text = f"""Hello {username},

Your monitored API '{api_name}' has failed 3 consecutive health checks and is marked as DOWN.

API Details:
- Name: {api_name}
- URL: {api_url}
- Last Error: {last_error}
- Detected At: {downtime_time}

Action Taken:
Automation has been paused (is_active = False) to prevent repeated failed requests.
Once your service is back online, please log in to your APIPulse dashboard and toggle automation back on.

Best regards,
APIPulse Monitoring Team
"""

        if not settings.smtp_user or not settings.smtp_password:
            return True

        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = settings.emails_from or settings.smtp_user
            msg["To"] = to_email

            msg.attach(MIMEText(plain_text, "plain"))

            if settings.smtp_port == 465:
                with smtplib.SMTP_SSL(settings.smtp_host, settings.smtp_port, timeout=10) as server:
                    server.login(settings.smtp_user, settings.smtp_password)
                    server.sendmail(msg["From"], [to_email], msg.as_string())
            else:
                with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=10) as server:
                    server.starttls()
                    server.login(settings.smtp_user, settings.smtp_password)
                    server.sendmail(msg["From"], [to_email], msg.as_string())

            return True
        except Exception:
            return False
