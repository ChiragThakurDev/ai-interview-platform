from app.services.email_service import EmailService


def send_welcome_email(email: str):
    subject = "Welcome to AI Interview Preparation Platform"

    body = f"""
Hi,

Welcome to the AI Interview Preparation Platform!

Your account has been created successfully.

We're excited to have you on board.

Happy Learning!

Regards,
AI Interview Platform Team
"""

    EmailService.send_email(
        to_email=email,
        subject=subject,
        body=body,
    )

    print(f"Welcome email sent to {email}")
