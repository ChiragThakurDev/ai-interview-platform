from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from app.core.config import settings


def _create_token(
    data: dict,
    expires_delta: timedelta,
    token_type: str,
):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + expires_delta

    to_encode.update(
        {
            "exp": expire,
            "type": token_type,
        }
    )

    return jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm,
    )


def create_access_token(data: dict):
    return _create_token(
        data=data,
        expires_delta=timedelta(
            minutes=settings.access_token_expire_minutes
        ),
        token_type="access",
    )


def create_refresh_token(data: dict):
    return _create_token(
        data=data,
        expires_delta=timedelta(
            days=settings.refresh_token_expire_days
        ),
        token_type="refresh",
    )


def create_email_verification_token(data: dict):
    return _create_token(
        data=data,
        expires_delta=timedelta(
            hours=settings.email_verification_expire_hours
        ),
        token_type="verify_email",
    )


def verify_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )

        return payload

    except JWTError as e:
        print("JWT ERROR:", e)
        return None
