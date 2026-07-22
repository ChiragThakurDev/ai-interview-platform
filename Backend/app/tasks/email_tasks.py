import logging

from app.tasks.celery_app import celery
from app.services.email_service import EmailService


logger = logging.getLogger(__name__)


@celery.task(
    name="send_welcome_email"
)
def send_welcome_email(
    email: str,
):

    try:

        subject = (
            "Welcome to AI Interview Preparation Platform"
        )

        body = f"""
Hi,

Welcome to the AI Interview Preparation Platform!

Your account has been created successfully.

We're excited to have you on board.

Happy Learning!

Regards,
AI Interview Platform Team
"""


        email_service = EmailService()


        email_service.send_email(
            to_email=email,
            subject=subject,
            body=body,
        )


        logger.info(
            f"Welcome email sent successfully to {email}"
        )


        return {
            "status": "success",
            "email": email,
        }


    except Exception as e:

        logger.error(
            f"Failed to send welcome email: {str(e)}"
        )

        raise e
