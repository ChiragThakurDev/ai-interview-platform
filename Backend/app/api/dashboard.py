from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


from app.db.dependencies import get_db
from app.dependencies.auth import get_current_user

from app.models.user import User

from app.schemas.dashboard import (
    DashboardResponse,
)

from app.services.dashboard_service import (
    DashboardService,
)



router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)



@router.get(
    "",
    response_model=DashboardResponse,
)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = DashboardService(db)

    return service.get_dashboard(
        current_user.id
    )
