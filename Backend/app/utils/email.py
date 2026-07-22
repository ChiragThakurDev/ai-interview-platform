import logging

from app.services.email_service import EmailService
from app.core.config import settings


logger = logging.getLogger(__name__)


# =====================================
# Core Email Sender
# =====================================

def send_email(
    to_email: str,
    subject: str,
    body: str
):

    try:

        EmailService.send_email(
            to_email=to_email,
            subject=subject,
            body=body,
        )


        logger.info(
            f"Email sent successfully to {to_email}"
        )


    except Exception as e:

        logger.error(
            f"Email sending failed to {to_email}: {str(e)}"
        )

        raise e



# =====================================
# Verification Email
# =====================================

def send_verification_email(
    to_email: str,
    token: str
):


    link = (
        f"{settings.frontend_url}"
        f"/verify-email?token={token}"
    )


    subject = (
        f"Verify your email - {settings.app_name}"
    )


    body = f"""

Hello,

Welcome to {settings.app_name}.


Please verify your email address:

{link}


This verification link will expire soon.


Thanks,
{settings.app_name} Team

"""


    send_email(
        to_email,
        subject,
        body
    )




# =====================================
# Reset Password Email
# =====================================

def send_reset_password_email(
    to_email: str,
    token: str
):


    link = (
        f"{settings.frontend_url}"
        f"/reset-password?token={token}"
    )


    subject = (
        f"Password Reset - {settings.app_name}"
    )


    body = f"""

Hello,


You requested a password reset.


Click the link below:

{link}


If you did not request this, please ignore this email.


Thanks,
{settings.app_name} Team

"""


    send_email(
        to_email,
        subject,
        body
    )
