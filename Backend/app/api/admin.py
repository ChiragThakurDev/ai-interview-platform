from fastapi import (
    APIRouter,
    Depends,
    Query,
)
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.dependencies.auth import get_current_admin

from app.models.user import User

from app.services.admin_service import (
    AdminService,
)
from app.schemas.admin import (
    AdminDashboardResponse,
    AdminUserResponse,
    RecentActivityResponse,
    PaginatedUsersResponse,
    AdminAnalyticsResponse,
)
router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


# =====================================================
# Dashboard Summary
# =====================================================

@router.get(
    "/dashboard",
    response_model=AdminDashboardResponse,
)
def get_dashboard(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):

    service = AdminService(db)

    return service.get_dashboard_summary()


# =====================================================
# Get All Users
# =====================================================

@router.get(
    "/users",
    response_model=list[AdminUserResponse],
)
def get_all_users(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):

    service = AdminService(db)

    return service.get_all_users()


# =====================================================
# Search Users (Pagination)
# =====================================================

@router.get(
    "/users/search",
    response_model=PaginatedUsersResponse,
)
def search_users(
    page: int = Query(
        1,
        ge=1,
    ),
    limit: int = Query(
        10,
        ge=1,
        le=100,
    ),
    search: str = "",
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):

    service = AdminService(db)

    return service.search_users(
        page=page,
        limit=limit,
        search=search,
    )


# =====================================================
# Get Single User
# =====================================================

@router.get(
    "/users/{user_id}",
    response_model=AdminUserResponse,
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):

    service = AdminService(db)

    return service.get_user(
        user_id
    )


# =====================================================
# Activate User
# =====================================================

@router.patch(
    "/users/{user_id}/activate",
    response_model=AdminUserResponse,
)
def activate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):

    service = AdminService(db)

    return service.activate_user(
        user_id
    )


# =====================================================
# Deactivate User
# =====================================================

@router.patch(
    "/users/{user_id}/deactivate",
    response_model=AdminUserResponse,
)
def deactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):

    service = AdminService(db)

    return service.deactivate_user(
        user_id
    )


# =====================================================
# Delete User
# =====================================================

@router.delete(
    "/users/{user_id}",
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):

    service = AdminService(db)

    return service.delete_user(
        user_id
    )


# =====================================================
# Recent Activity
# =====================================================

@router.get(
    "/activity",
    response_model=RecentActivityResponse,
)
def get_recent_activity(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):

    service = AdminService(db)

    return service.get_recent_activity()

# =====================================================
# Admin Analytics
# =====================================================

@router.get(
    "/analytics",
    response_model=AdminAnalyticsResponse,
)
def get_analytics(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):

    service = AdminService(db)

    return service.get_analytics()
