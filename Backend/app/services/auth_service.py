import time

from app.core.config import settings

from app.repositories.user_repository import UserRepository

from app.utils.security import (
        verify_password,
        hash_password,
        )

from app.utils.jwt import (
        create_access_token,
        create_refresh_token,
        create_password_reset_token,
        verify_access_token,
        )

from app.utils.refresh_token_store import (
        store_refresh_token,
        is_refresh_token_valid,
        rotate_refresh_token,
        )

from app.utils.rate_limiter import (
        increment_login_attempts,
        reset_login_attempts,
        is_login_blocked,
        )

from app.utils.token_blacklist import blacklist_token

from app.utils.email import send_reset_password_email

from app.core.exceptions import AuthException
from app.core.logger import logger


class AuthService:

    def __init__(self, db):
        self.repository = UserRepository(db)


    # -------------------------
    # LOGIN
    # -------------------------
    def login(self, email: str, password: str):

        user = self.repository.get_by_email(email)

        if not user:
            logger.warning(
                    f"Failed login attempt: user '{email}' not found."
                    )

            increment_login_attempts(email)

            raise AuthException.invalid_credentials()


        if not verify_password(password, user.password_hash):

            logger.warning(
                    f"Failed login attempt: incorrect password for '{email}'."
                    )

            increment_login_attempts(email)

            raise AuthException.invalid_credentials()


        access_token = create_access_token(
             {
                 "sub": user.email,
                 "user_id": user.id,
                 }
             )

        refresh_token = create_refresh_token(
             {
                 "sub": user.email,
                 "user_id": user.id,
                 }
             ) 

        store_refresh_token(
             token=refresh_token,
             expires_in=settings.refresh_token_expire_days * 24 * 60 * 60,
             )


        logger.info(
             f"User '{user.email}' logged in successfully."
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

            logger.warning(
                    "Invalid refresh token."
                    )

            raise AuthException.invalid_token()


        if payload.get("type") != "refresh":

            logger.warning(
                    "Invalid refresh token type."
                    )

            raise AuthException.invalid_token()



        if not is_refresh_token_valid(refresh_token):

            logger.warning(
                    "Refresh token not found or expired."
                    )

            raise AuthException.invalid_token()



        email = payload.get("sub")


        if email is None:

            raise AuthException.invalid_token()



        user = self.repository.get_by_email(email)


        if user is None:

            raise AuthException.not_found()



        new_access_token = create_access_token(
                {
                    "sub": user.email,
                    "user_id":user.id,
                    }
                )


        new_refresh_token = create_refresh_token(
                {
                    "sub": user.email,
                    "user_id":user.id,
                    }
                )


        rotate_refresh_token(
                old_token=refresh_token,
                new_token=new_refresh_token,
                expires_in=settings.refresh_token_expire_days * 24 * 60 * 60,
                )


        logger.info(
                f"Access token refreshed for '{user.email}'."
                )


        return {
                "access_token": new_access_token,
                "refresh_token": new_refresh_token,
                "token_type": "bearer",
                }



    # -------------------------
    # VERIFY EMAIL
    # -------------------------
    def verify_email(self, token: str):

        payload = verify_access_token(
                token.strip()
                )


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


        logger.info(
                f"Email verified for '{user.email}'."
                )


        return {
                "message": "Email verified successfully"
                }



    # -------------------------
    # FORGOT PASSWORD
    # -------------------------
    def forgot_password(
            self,
            email: str,
            background_tasks
            ):

        user = self.repository.get_by_email(email)


        if user is None:

            logger.warning(
                    f"Password reset requested for unknown email '{email}'."
                    )

            return {
                    "message":
                    "If the email exists, a password reset link has been sent."
                    }



        reset_token = create_password_reset_token(
                {
                    "sub": user.email
                    }
                )


        background_tasks.add_task(
                send_reset_password_email,
                user.email,
                reset_token
                )


        logger.info(
                f"Password reset email sent to '{user.email}'."
                )


        return {
                "message":
                "If the email exists, a password reset link has been sent."
                }



    # -------------------------
    # RESET PASSWORD
    # -------------------------
    def reset_password(
            self,
            token: str,
            new_password: str
            ):

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



        user.password_hash = hash_password(
                new_password
                )


        self.repository.update(user)


        logger.info(
                f"Password reset successfully for '{user.email}'."
                )


        return {
                "message":
                "Password reset successfully"
                }



    # -------------------------
    # LOGOUT
    # -------------------------
    def logout(self, token: str):

        # FIX: missing token handling
        if token is None:

            logger.warning(
                    "Logout attempted without token."
                    )

            raise AuthException.invalid_token()



        payload = verify_access_token(token)


        if payload is None:

            raise AuthException.invalid_token()



        exp = payload.get("exp")


        if exp is None:

            raise AuthException.invalid_token()



        expires_in = exp - int(time.time())


        if expires_in > 0:

            blacklist_token(
                    token,
                    expires_in
                    )



        email = payload.get("sub")


        logger.info(
                f"User '{email}' logged out successfully."
                )


        return {
                "message":
                "Logged out successfully"
                }
