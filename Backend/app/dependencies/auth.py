from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.db.session import get_db
from app.repositories.user_repository import UserRepository
from app.utils.jwt import verify_access_token

from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    payload = verify_access_token(token)

    if payload is None:
        raise ValueError("Invalid token")

    email = payload.get("sub")

    if email is None:
        raise ValueError("Invalid token")

    repository = UserRepository(db)

    user = repository.get_by_email(email)

    if user is None:
        raise ValueError("User not found")

    return user
