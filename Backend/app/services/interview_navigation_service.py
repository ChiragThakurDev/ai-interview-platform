from sqlalchemy.orm import Session

from app.services.interview_question_service import (
    InterviewQuestionService,
)


class InterviewNavigationService:
    """
    Handles interview question navigation.
    """

    def __init__(self, db: Session):
        self.question_service = InterviewQuestionService(db)

    # =====================================================
    # Current Question
    # =====================================================

    def get_current_question(
        self,
        question_id: int,
    ):
        return self.question_service.get_question(
            question_id
        )

    # =====================================================
    # Next Question
    # =====================================================

    def get_next_question(
        self,
        interview_id: int,
        current_question_id: int,
    ):
        return self.question_service.get_next_question(
            interview_id,
            current_question_id,
        )

    # =====================================================
    # Is Last Question
    # =====================================================

    def is_last_question(
        self,
        interview_id: int,
        current_question_id: int,
    ) -> bool:

        return (
            self.get_next_question(
                interview_id,
                current_question_id,
            )
            is None
        )
