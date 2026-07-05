from datetime import datetime, timezone

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db

from app.repositories.api_key_repository import APIKeyRepository
from app.repositories.user_repository import UserRepository

from app.utils.api_key import hash_api_key


def get_api_key_user(
    api_key: str = Header(..., alias="X-API-Key"),
    db: Session = Depends(get_db),
):
    # Create repository
    api_key_repository = APIKeyRepository(db)

    # Hash incoming API Key
    hashed_key = hash_api_key(api_key)

    # Find API Key in database
    api_key_obj = api_key_repository.get_by_hash(hashed_key)

    if api_key_obj is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )

    # Check if revoked
    if not api_key_obj.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key has been revoked",
        )

    # Check expiration
    if (
        api_key_obj.expires_at is not None
        and api_key_obj.expires_at < datetime.now(timezone.utc)
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key has expired",
        )

    # Load owner of the API Key
    user_repository = UserRepository(db)

    user = user_repository.get_by_id(api_key_obj.user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    # Optional: Don't allow inactive users
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is inactive",
        )

    return user
