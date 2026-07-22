from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.dependencies.auth import get_current_active_user

from app.models.user import User

from app.schemas.interview_result import (
    InterviewResultResponse,
)

from app.services.interview_result_service import (
    InterviewResultService,
)


router = APIRouter(
    prefix="/interviews",
    tags=["Interview Results"],
)


# =====================================================
# Get Interview Result
# =====================================================

@router.get(
    "/{interview_id}/result",
    response_model=InterviewResultResponse,
)
def get_interview_result(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):

    service = InterviewResultService(db)

    return service.get_result(
        interview_id=interview_id,
        current_user=current_user,
    )
