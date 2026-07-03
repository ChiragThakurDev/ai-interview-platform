from app.repositories.user_repository import UserRepository
from app.utils.security import (
    verify_password,
    hash_password,
)

from app.utils.jwt import (
    create_access_token,
    create_refresh_token,
    create_email_verification_token,
    create_password_reset_token,
    verify_access_token,
)

from app.utils.email import (
    send_verification_email,
    send_reset_password_email,
)

from app.core.exceptions import AuthException

from app.utils.token_blacklist import blacklist_token
class AuthService:

    def __init__(self, db):
        self.repository = UserRepository(db)

    # -------------------------
    # LOGIN
    # -------------------------
    def login(self, email: str, password: str):
        user = self.repository.get_by_email(email)

        if not user:
            raise AuthException.invalid_credentials()

        if not verify_password(password, user.password_hash):
            raise AuthException.invalid_credentials()

        access_token = create_access_token(
            {"sub": user.email}
        )

        refresh_token = create_refresh_token(
            {"sub": user.email}
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    # -------------------------
    # REFRESH TOKEN
    # -------------------------
    def refresh_access_token(self, refresh_token: str):
        payload = verify_access_token(refresh_token)

        if payload is None:
            raise AuthException.invalid_token()

        if payload.get("type") != "refresh":
            raise AuthException.invalid_token()

        email = payload.get("sub")

        if email is None:
            raise AuthException.invalid_token()

        user = self.repository.get_by_email(email)

        if user is None:
            raise AuthException.not_found()

        access_token = create_access_token(
            {"sub": user.email}
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    # -------------------------
    # VERIFY EMAIL
    # -------------------------
    def verify_email(self, token: str):
        token = token.strip()

        payload = verify_access_token(token)

        if payload is None:
            raise AuthException.invalid_token()

        if payload.get("type") != "verify_email":
            raise AuthException.invalid_token()

        email = payload.get("sub")

        if email is None:
            raise AuthException.invalid_token()

        user = self.repository.get_by_email(email)

        if user is None:
            raise AuthException.not_found()

        if user.is_verified:
            return {
                "message": "Email already verified"
            }

        user.is_verified = True
        self.repository.update(user)

        return {
            "message": "Email verified successfully"
        }

    # -------------------------
    # FORGOT PASSWORD
    # -------------------------
    def forgot_password(self, email: str):
        user = self.repository.get_by_email(email)

        # Always return same response (security best practice)
        if user is None:
            return {
                "message": "If the email exists, a password reset link has been sent."
            }

        reset_token = create_password_reset_token(
            {"sub": user.email}
        )

        send_reset_password_email(user.email, reset_token)

        return {
            "message": "If the email exists, a password reset link has been sent."
        }

    # -------------------------
    # RESET PASSWORD
    # -------------------------
    def reset_password(self, token: str, new_password: str):
        payload = verify_access_token(token)

        if payload is None:
            raise AuthException.invalid_token()

        if payload.get("type") != "reset_password":
            raise AuthException.invalid_token()

        email = payload.get("sub")

        if email is None:
            raise AuthException.invalid_token()

        user = self.repository.get_by_email(email)

        if user is None:
            raise AuthException.not_found()

        user.password_hash = hash_password(new_password)
        self.repository.update(user)

        return {
            "message": "Password reset successfully"
        }



    def logout(self, token: str):
        payload = verify_access_token(token)

        if payload is None:
          raise ValueError("Invalid token")

        exp = payload.get("exp")

        if exp is None:
          raise ValueError("Token has no expiration")

        import time

        expires_in = exp - int(time.time())

        if expires_in > 0:
          blacklist_token(token, expires_in)

        return {
            "message": "Logged out successfully"
        }
