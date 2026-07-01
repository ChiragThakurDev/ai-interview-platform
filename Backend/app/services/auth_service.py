from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest
from app.utils.security import verify_password
from app.utils.jwt import create_access_token

class AuthService:

    def __init__(self,db):
        self.repository=UserRepository(db)


    def login(self,login_data:LoginRequest):
        user=self.repository.get_by_email(login_data.email)

        if not user:
            raise ValueError("Invalid email or password")


        if not verify_password(
                login_data.password,
                user.password_hash,
        ):
            raise ValueError("Invalid email or password")

        token =create_access_token(
                {
                    "sub":user.email
                    }
                )
        return{
                "access_token":token,
                "token_type":"bearer",
            }


