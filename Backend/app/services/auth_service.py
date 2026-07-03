from app.repositories.user_repository import UserRepository
from app.utils.security import verify_password
from app.utils.jwt import (
    create_access_token,
    create_refresh_token,
    create_email_verification_token,
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
