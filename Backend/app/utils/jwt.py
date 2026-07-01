from datetime import datetime, timedelta, timezone

from jose import jwt, JWTError

from app.core.config import settings

def create_access_token(data:dict):
    to_encode=data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
            )

    to_encode.update({"exp":expire})


    encode_jwt =jwt.encode(
            to_encode,
            settings.secret_key,
            algorithm=settings.algorithm,
            )

    return encode_jwt

def verify_access_token(token:str):
    try:
        payload=jwt.decode(
                token,
                settings.secret_key,
                algorithms=[settings.algorithm]
                )

        return payload

    except JWTError:
        return None


