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
        if not settings.smtp_user or not settings.smtp_password:
            raise smtplib.SMTPAuthenticationError(
                535, "SMTP credentials are not configured or invalid."
            )

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

        html_content = f"""<!DOCTYPE html>
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px;">
        <h2 style="color: #e53e3e; margin-top: 0;">🚨 API Downtime Alert</h2>
        <p>Hello <strong>{username}</strong>,</p>
        <p>Your monitored API <strong>{api_name}</strong> has failed <strong>3 consecutive health checks</strong> and is marked as <strong>DOWN</strong>.</p>
        
        <div style="background-color: #fff5f5; border-left: 4px solid #e53e3e; padding: 12px 16px; margin: 16px 0;">
            <p style="margin: 4px 0;"><strong>Endpoint:</strong> <code>{api_url}</code></p>
            <p style="margin: 4px 0;"><strong>Last Error:</strong> <span style="color: #c53030;">{last_error}</span></p>
            <p style="margin: 4px 0;"><strong>Detected At:</strong> {downtime_time}</p>
        </div>

        <div style="background-color: #f7fafc; padding: 12px 16px; border-radius: 6px; margin-top: 16px;">
            <p style="margin: 0; font-size: 14px; color: #4a5568;">
                ⚠️ <strong>Action Taken:</strong> Automation has been paused (<code>is_active = False</code>) to prevent request spam.
                Once your service is restored, re-enable automation from your dashboard.
            </p>
        </div>

        <hr style="border: none; border-top: 1px solid #eee; margin: 24px 0;" />
        <p style="font-size: 12px; color: #a0aec0; text-align: center;">Sent automatically by APIPulse Monitoring Engine</p>
    </div>
</body>
</html>"""

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = settings.emails_from or settings.smtp_user
        msg["To"] = to_email

        msg.attach(MIMEText(plain_text, "plain"))
        msg.attach(MIMEText(html_content, "html"))

        try:
            if settings.smtp_port == 465:
                with smtplib.SMTP_SSL(settings.smtp_host, settings.smtp_port, timeout=10) as server:
                    server.login(settings.smtp_user, settings.smtp_password)
                    server.send_message(msg)
            else:
                with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=10) as server:
                    server.starttls()
                    server.login(settings.smtp_user, settings.smtp_password)
                    server.send_message(msg)

            return True
        except smtplib.SMTPException:
            raise
        except (ConnectionError, OSError, TimeoutError) as e:
            raise smtplib.SMTPConnectError(421, f"Failed to connect to SMTP server: {str(e)}")
