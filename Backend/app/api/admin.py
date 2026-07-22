from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.dependencies.auth import get_current_admin

from app.models.user import User

from app.services.admin_service import AdminService


router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


# =====================================================
# Dashboard Summary
# =====================================================

@router.get("/dashboard")
def dashboard(
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    service = AdminService(db)

    return service.get_dashboard_summary()


# =====================================================
# Recent Activity
# =====================================================

@router.get("/activity")
def activity(
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    service = AdminService(db)

    return service.get_recent_activity()


# =====================================================
# Get All Users
# =====================================================

@router.get("/users")
def users(
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    service = AdminService(db)

    return service.get_all_users()


# =====================================================
# Search Users
# =====================================================

@router.get("/users/search")
def search_users(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str = "",
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    service = AdminService(db)

    return service.search_users(
        page=page,
        limit=limit,
        search=search,
    )


# =====================================================
# Activate User
# =====================================================

@router.patch("/users/{user_id}/activate")
def activate_user(
    user_id: int,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    service = AdminService(db)

    return service.activate_user(user_id)


# =====================================================
# Deactivate User
# =====================================================

@router.patch("/users/{user_id}/deactivate")
def deactivate_user(
    user_id: int,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    service = AdminService(db)

    return service.deactivate_user(user_id)


# =====================================================
# Delete User
# =====================================================

@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    service = AdminService(db)

    return service.delete_user(user_id)


# =====================================================
# Analytics
# =====================================================

@router.get("/analytics")
def analytics(
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    service = AdminService(db)

    return service.get_analytics()
