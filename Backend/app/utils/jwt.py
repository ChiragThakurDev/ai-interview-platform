from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from app.core.config import settings


def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + expires_delta

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm,
    )


def create_access_token(data: dict):
    return create_token(
        data,
        timedelta(minutes=settings.access_token_expire_minutes),
    )


def create_refresh_token(data: dict):
    return create_token(
        data,
        timedelta(days=settings.refresh_token_expire_days),
    )


def verify_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        return payload

    except JWTError:
        return None
