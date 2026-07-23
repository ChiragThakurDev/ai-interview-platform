from fastapi import BackgroundTasks
from sqlalchemy.orm import Session

from app.models.user import User

from app.repositories.user_repository import UserRepository

from app.schemas.user import UserCreate

from app.utils.security import hash_password

from app.core.exceptions import AuthException

from app.utils.jwt import create_email_verification_token

from app.utils.email import send_verification_email



class UserService:


    def __init__(
        self,
        db: Session
    ):
        self.repository = UserRepository(db)



    # =========================================
    # CREATE USER
    # =========================================

    def create_user(
        self,
        user_data: UserCreate,
        background_tasks:BackgroundTasks | None =None,
    ) -> User:


        existing_user = self.repository.get_by_email(
            user_data.email
        )


        if existing_user:

            raise ValueError(
                "Email already registered"
            )



        user = User(

            name=user_data.name,

            email=user_data.email,

            password_hash=hash_password(
                user_data.password
            ),

            is_verified=False,

            is_active=True,

        )


        created_user = self.repository.create(
            user
        )



        # ==============================
        # EMAIL VERIFICATION TOKEN
        # ==============================


        token = create_email_verification_token(
            {
                "sub": created_user.email
            }
        )


        if background_tasks:
            background_tasks.add_task(

              send_verification_email,

              created_user.email,

              token

            )




        return created_user





    # =========================================
    # GET ALL USERS
    # =========================================

    def get_all_users(self):

        return self.repository.get_all()





    # =========================================
    # ACTIVATE USER
    # =========================================

    def activate_user(
        self,
        user_id:int
    ):


        user = self.repository.get_by_id(
            user_id
        )


        if user is None:

            raise AuthException.not_found()



        user.is_active=True


        self.repository.update(
            user
        )


        return {

            "message":
            "User activated successfully"

        }





    # =========================================
    # DEACTIVATE USER
    # =========================================

    def deactivate_user(
        self,
        user_id:int
    ):


        user = self.repository.get_by_id(
            user_id
        )


        if user is None:

            raise AuthException.not_found()



        user.is_active=False


        self.repository.update(
            user
        )


        return {

            "message":
            "User deactivated successfully"

        }





    # =========================================
    # DELETE USER
    # =========================================

    def delete_user(
        self,
        user_id:int
    ):


        user = self.repository.get_by_id(
            user_id
        )


        if user is None:

            raise AuthException.not_found()



        self.repository.delete(
            user
        )


        return {

            "message":
            "User deleted successfully"

        }
