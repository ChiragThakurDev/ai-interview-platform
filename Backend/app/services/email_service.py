import smtplib
import logging

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import settings


logger = logging.getLogger(__name__)


class EmailService:

    @staticmethod
    def send_email(
        to_email: str,
        subject: str,
        body: str,
        html: bool = False,
    ):

        try:

            message = MIMEMultipart()

            message["From"] = settings.smtp_email
            message["To"] = to_email
            message["Subject"] = subject


            content_type = "html" if html else "plain"


            message.attach(
                MIMEText(
                    body,
                    content_type,
                )
            )


            with smtplib.SMTP(
                settings.smtp_host,
                settings.smtp_port,
                timeout=10,
            ) as server:


                server.starttls()


                server.login(
                    settings.smtp_email,
                    settings.smtp_password,
                )


                server.send_message(
                    message
                )


            logger.info(
                f"Email sent successfully to {to_email}"
            )


            return True


        except smtplib.SMTPException as e:

            logger.error(
                f"SMTP error while sending email to {to_email}: {str(e)}"
            )

            raise e


        except Exception as e:

            logger.error(
                f"Unexpected email error: {str(e)}"
            )

            raise e
