from sqlalchemy.orm import Session

from app.models.api_key import APIKey


class APIKeyRepository:

    def __init__(self, db: Session):
        self.db = db

    # -------------------------
    # Create API Key
    # -------------------------
    def create(self, api_key: APIKey) -> APIKey:
        self.db.add(api_key)
        self.db.commit()
        self.db.refresh(api_key)
        return api_key

    # -------------------------
    # Get API Key by ID
    # -------------------------
    def get_by_id(self, api_key_id: int) -> APIKey | None:
        return (
            self.db.query(APIKey)
            .filter(APIKey.id == api_key_id)
            .first()
        )

    # -------------------------
    # Get API Key by Hash
    # -------------------------
    def get_by_hash(self, key_hash: str) -> APIKey | None:
        return (
            self.db.query(APIKey)
            .filter(APIKey.key_hash == key_hash)
            .first()
        )

    # -------------------------
    # Get All API Keys of User
    # -------------------------
    def get_all_by_user(self, user_id: int) -> list[APIKey]:
        return (
            self.db.query(APIKey)
            .filter(APIKey.user_id == user_id)
            .all()
        )

    # -------------------------
    # Update API Key
    # -------------------------
    def update(self, api_key: APIKey) -> APIKey:
        self.db.commit()
        self.db.refresh(api_key)
        return api_key

    # -------------------------
    # Delete API Key
    # -------------------------
    def delete(self, api_key: APIKey) -> None:
        self.db.delete(api_key)
        self.db.commit()
