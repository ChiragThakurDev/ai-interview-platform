from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User

from app.repositories.interview_result_repository import (
    InterviewResultRepository,
)


class InterviewResultService:

    def __init__(
        self,
        db: Session,
    ):
        self.repository = InterviewResultRepository(db)

    # =====================================================
    # Get Interview Result
    # =====================================================

    def get_result(
        self,
        interview_id: int,
        current_user: User,
    ):

        interview = self.repository.get_interview(
            interview_id
        )

        if interview is None:
            raise HTTPException(
                status_code=404,
                detail="Interview not found",
            )

        if interview.user_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="Not authorized to view this interview",
            )

        answers = self.repository.get_answers(
            interview_id
        )

        report = self.repository.get_report(
            interview_id
        )

        return {
            "interview": interview,
            "questions": answers,
            "report": report,
        }
