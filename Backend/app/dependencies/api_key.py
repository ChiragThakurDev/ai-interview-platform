from datetime import datetime, timezone

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db

from app.models.api_key import APIKey

from app.repositories.api_key_repository import APIKeyRepository
from app.repositories.user_repository import UserRepository

from app.utils.api_key import hash_api_key


# =====================================================
# Return API Key Object
# =====================================================

def get_current_api_key(
    api_key: str = Header(..., alias="X-API-Key"),
    db: Session = Depends(get_db),
) -> APIKey:

    api_key_repository = APIKeyRepository(db)

    hashed_key = hash_api_key(api_key)

    api_key_obj = api_key_repository.get_by_hash(hashed_key)

    if api_key_obj is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )

    if not api_key_obj.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key has been revoked",
        )

    if (
        api_key_obj.expires_at is not None
        and api_key_obj.expires_at < datetime.now(timezone.utc)
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key has expired",
        )

    return api_key_obj


# =====================================================
# Return User From API Key
# =====================================================

def get_api_key_user(
    api_key: APIKey = Depends(get_current_api_key),
    db: Session = Depends(get_db),
):
    user_repository = UserRepository(db)

    user = user_repository.get_by_id(api_key.user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is inactive",
        )

    return user
