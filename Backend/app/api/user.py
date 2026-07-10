from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    BackgroundTasks,
)
from app.tasks.email_tasks import send_welcome_email
from sqlalchemy.orm import Session

from app.dependencies.auth import (
    get_current_user,
    get_current_admin,
)

from app.db.dependencies import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService
from app.models.user import User

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


# -------------------------
# REGISTER
# -------------------------
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    service = UserService(db)

    try:
        created_user=service.create_user(user)

        background_tasks.add_task(
                send_welcome_email,
                create_user.email,
            )
        return created_user

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# -------------------------
# CURRENT USER
# -------------------------
@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user),
):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role,
        "is_active": current_user.is_active,
    }


# -------------------------
# ADMIN DASHBOARD
# -------------------------
@router.get("/admin")
def admin_dashboard(
    current_admin: User = Depends(get_current_admin),
):
    return {
        "message": "Welcome Admin!",
        "id": current_admin.id,
        "name": current_admin.name,
        "email": current_admin.email,
        "role": current_admin.role,
    }


# -------------------------
# GET ALL USERS (Admin)
# -------------------------
@router.get("/")
def get_all_users(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    service = UserService(db)
    return service.get_all_users()


# -------------------------
# ACTIVATE USER (Admin)
# -------------------------
@router.patch("/{user_id}/activate")
def activate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    service = UserService(db)
    return service.activate_user(user_id)


# -------------------------
# DEACTIVATE USER (Admin)
# -------------------------
@router.patch("/{user_id}/deactivate")
def deactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    service = UserService(db)
    return service.deactivate_user(user_id)


# -------------------------
# DELETE USER (Admin)
# -------------------------
@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    service = UserService(db)
    return service.delete_user(user_id)
