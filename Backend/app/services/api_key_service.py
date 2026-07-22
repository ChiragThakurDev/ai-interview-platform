from sqlalchemy.orm import Session

from app.models.api_key import APIKey
from app.models.user import User

from app.repositories.api_key_repository import APIKeyRepository

from app.schemas.api_key import APIKeyCreate

from app.utils.api_key import (
    generate_api_key,
    hash_api_key,
)


class APIKeyService:

    def __init__(self, db: Session):
        self.repository = APIKeyRepository(db)

    # -------------------------
    # Create API Key
    # -------------------------
    def create_api_key(
        self,
        current_user: User,
        request: APIKeyCreate,
    ):
        # Generate a secure API key
        plain_api_key = generate_api_key()

        # Hash it before storing
        hashed_key = hash_api_key(plain_api_key)

        # Save to database
        api_key = APIKey(
            key_hash=hashed_key,
            name=request.name,
            permissions=request.permissions,
            user_id=current_user.id,
            is_active=True,
        )

        api_key = self.repository.create(api_key)

        # Return the plain API key ONLY ONCE
        return {
            "id": api_key.id,
            "name": api_key.name,
            "api_key": plain_api_key,
            "permissions": api_key.permissions,
            "is_active": api_key.is_active,
            "expires_at": api_key.expires_at,
            "created_at": api_key.created_at,
        }

    # -------------------------
    # List User API Keys
    # -------------------------
    def list_api_keys(
        self,
        current_user: User,
    ):
        return self.repository.get_all_by_user(current_user.id)

    # -------------------------
    # Delete API Key
    # -------------------------
    def revoke_api_key(
        self,
        api_key_id: int,
        current_user: User,
    ):
        api_key = self.repository.get_by_id(api_key_id)

        if api_key is None:
            raise ValueError("API Key not found.")

        if api_key.user_id != current_user.id:
            raise ValueError("You cannot delete another user's API Key.")

        self.repository.delete(api_key)

        return {
            "message": "API Key revoked successfully."
        }

    # -------------------------
    # Get Single API Key
    # -------------------------
    def get_api_key(
        self,
        api_key_id: int,
        current_user: User,
    ):
        api_key = self.repository.get_by_id(api_key_id)

        if api_key is None:
            raise ValueError("API Key not found.")

        if api_key.user_id != current_user.id:
            raise ValueError("You cannot access another user's API Key.")

        return api_key
