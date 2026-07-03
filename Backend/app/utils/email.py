import smtplib
from email.message import EmailMessage

from app.core.config import settings


def send_email(to_email: str, subject: str, body: str):
    msg = EmailMessage()
    msg["From"] = settings.smtp_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as smtp:
        smtp.starttls()
        smtp.login(settings.smtp_email, settings.smtp_password)
        smtp.send_message(msg)


# -----------------------------
# Helper 1: Verification Email
# -----------------------------
def send_verification_email(to_email: str, token: str):
    link = f"http://127.0.0.1:8000/auth/verify-email?token={token}"

    subject = "Verify your email"
    body = f"""
Hello,

Please verify your email by clicking the link below:

{link}

This link will expire soon.

Thanks,
AI Interview Platform
"""

    send_email(to_email, subject, body)


# -----------------------------
# Helper 2: Reset Password Email
# -----------------------------
def send_reset_password_email(to_email: str, token: str):
    link = f"http://127.0.0.1:8000/auth/reset-password?token={token}"

    subject = "Reset your password"
    body = f"""
Hello,

Click below to reset your password:

{link}

If this wasn't you, ignore this email.

Thanks,
AI Interview Platform
"""

    send_email(to_email, subject, body)
