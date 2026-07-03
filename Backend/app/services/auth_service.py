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


class AuthService:

    def __init__(self, db):
        self.repository = UserRepository(db)

    def login(self, email: str, password: str):
        user = self.repository.get_by_email(email)

        if not user:
            raise ValueError("Invalid email or password")

        if not verify_password(
            password,
            user.password_hash,
        ):
            raise ValueError("Invalid email or password")

        access_token = create_access_token(
            {
                "sub": user.email,
            }
        )

        refresh_token = create_refresh_token(
            {
                "sub": user.email,
            }
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    def refresh_access_token(self, refresh_token: str):
        payload = verify_access_token(refresh_token)

        if payload is None:
            raise ValueError("Invalid refresh token")

        if payload.get("type") != "refresh":
            raise ValueError("Invalid token type")

        email = payload.get("sub")

        if email is None:
            raise ValueError("Invalid refresh token")

        user = self.repository.get_by_email(email)

        if user is None:
            raise ValueError("User not found")

        access_token = create_access_token(
            {
                "sub": user.email,
            }
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    def verify_email(self, token: str):
        print("\n======================")
        print("Received token:", repr(token))

        token = token.strip()

        payload = verify_access_token(token)

        print("Decoded payload:", payload)
        print("======================\n")

        if payload is None:
            raise ValueError("Invalid verification token")

        if payload.get("type") != "verify_email":
            raise ValueError("Invalid token type")

        email = payload.get("sub")

        if email is None:
            raise ValueError("Invalid verification token")

        user = self.repository.get_by_email(email)

        if user is None:
            raise ValueError("User not found")

        if user.is_verified:
            raise ValueError("Email already verified")

        user.is_verified = True

        self.repository.update(user)

        return {
            "message": "Email verified successfully"
        }

    def forgot_password(self, email: str):
        user = self.repository.get_by_email(email)

        # Prevent email enumeration
        if user is None:
            return {
                "message": "If the email exists, a password reset link has been sent."
            }

        reset_token = create_password_reset_token(
            {
                "sub": user.email,
            }
        )

        return {
            "message": "Password reset token generated successfully.",
            "reset_token": reset_token,
        }

    def reset_password(
        self,
        token: str,
        new_password: str,
    ):
        # Verify token
        payload = verify_access_token(token)

        if payload is None:
            raise ValueError("Invalid reset token")

        # Only password reset tokens are allowed
        if payload.get("type") != "reset_password":
            raise ValueError("Invalid token type")

        email = payload.get("sub")

        if email is None:
            raise ValueError("Invalid reset token")

        # Find user
        user = self.repository.get_by_email(email)

        if user is None:
            raise ValueError("User not found")

        # Hash new password
        user.password_hash = hash_password(new_password)

        # Save changes
        self.repository.update(user)

        return {
            "message": "Password reset successfully"
        }
