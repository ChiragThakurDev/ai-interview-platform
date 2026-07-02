from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService

from app.auth.dependencies import get_current_user

from app.auth.dependencies import get_current_admin
from app.models.user import User

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    service = UserService(db)

    try:
        return service.create_user(user)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


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

@router.get("/admin")
def admin_dashboard(
        current_admin: User=Depends(get_current_admin),
):
    return {
            "message":"Welcome Admin!",
            "admin":current_admin.name,
            "email":current_admin.email,
            }
