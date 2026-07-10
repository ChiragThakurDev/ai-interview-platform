import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import settings


class EmailService:
    @staticmethod
    def send_email(
        to_email: str,
        subject: str,
        body: str,
    ):
        message = MIMEMultipart()

        message["From"] = settings.smtp_email
        message["To"] = to_email
        message["Subject"] = subject

        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(
            settings.smtp_host,
            settings.smtp_port,
        ) as server:
            server.starttls()

            server.login(
                settings.smtp_email,
                settings.smtp_password,
            )

            server.send_message(message)

        print(f"Email sent successfully to {to_email}")
