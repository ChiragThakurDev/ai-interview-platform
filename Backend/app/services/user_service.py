from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.utils.security import hash_password

class UserService:
    def __init__(self,db:Session):
        self.repository=UserRepository(db)

    def create_user(self, user_data:UserCreate) -> User:

        existing_user=self.repository.get_by_email(user_data.email)

        if existing_user:
            raise ValueError("Email already registered")

        user=User(
                name=user_data.name,
                email=user_data.email,
                password_hash=hash_password(user_data.password),
                )
        return self.repository.create(user)
