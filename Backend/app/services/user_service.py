from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.utils.security import hash_password
from app.core.exceptions import AuthException


class UserService:

    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    # -------------------------
    # CREATE USER
    # -------------------------
    def create_user(self, user_data: UserCreate) -> User:

        existing_user = self.repository.get_by_email(user_data.email)

        if existing_user:
            raise ValueError("Email already registered")

        user = User(
            name=user_data.name,
            email=user_data.email,
            password_hash=hash_password(user_data.password),
        )

        return self.repository.create(user)

    # -------------------------
    # GET ALL USERS
    # -------------------------
    def get_all_users(self):
        return self.repository.get_all()

    # -------------------------
    # ACTIVATE USER
    # -------------------------
    def activate_user(self, user_id: int):

        user = self.repository.get_by_id(user_id)

        if user is None:
            raise AuthException.not_found()

        user.is_active = True

        self.repository.update(user)

        return {
            "message": "User activated successfully"
        }

    # -------------------------
    # DEACTIVATE USER
    # -------------------------
    def deactivate_user(self, user_id: int):

        user = self.repository.get_by_id(user_id)

        if user is None:
            raise AuthException.not_found()

        user.is_active = False

        self.repository.update(user)

        return {
            "message": "User deactivated successfully"
        }

    # -------------------------
    # DELETE USER
    # -------------------------
    def delete_user(self, user_id: int):

        user = self.repository.get_by_id(user_id)

        if user is None:
            raise AuthException.not_found()

        self.repository.delete(user)

        return {
            "message": "User deleted successfully"
        }
