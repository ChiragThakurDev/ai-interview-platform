from sqlalchemy.orm import Session

from app.models.interview_answer import InterviewAnswer
from app.repositories.interview_answer_repository import (
    InterviewAnswerRepository,
)


class InterviewAnswerService:

    def __init__(
        self,
        db: Session,
    ):
        self.repository = InterviewAnswerRepository(db)


    # =====================================================
    # Create Answer
    # =====================================================

    def create_answer(
        self,
        interview_id: int,
        question_id: int,
        answer: str,
        score: int,
        feedback: str,
    ):

        interview_answer = InterviewAnswer(
            interview_id=interview_id,
            question_id=question_id,
            answer=answer,
            score=score,
            feedback=feedback,
        )

        return self.repository.create(
            interview_answer
        )


    # =====================================================
    # Update Answer
    # =====================================================

    def update_answer(
        self,
        interview_answer: InterviewAnswer,
        answer: str,
        score: int,
        feedback: str,
    ):

        return self.repository.update(
            interview_answer,
            answer,
            score,
            feedback,
        )


    # =====================================================
    # Get Answer By Question
    # =====================================================

    def get_answer(
        self,
        question_id: int,
    ):

        return self.repository.get_by_question(
            question_id
        )


    # =====================================================
    # Delete Answer
    # =====================================================

    def delete_answer(
        self,
        interview_answer: InterviewAnswer,
    ):

        self.repository.delete(
            interview_answer
        )
