from sqlalchemy.orm import Session

from app.models.interview_question import InterviewQuestion

from app.repositories.interview_question_repository import (
    InterviewQuestionRepository,
)


class InterviewQuestionService:

    def __init__(
        self,
        db: Session,
    ):

        self.repository = (
            InterviewQuestionRepository(db)
        )

    # =====================================================
    # Create Questions
    # =====================================================

    def create_questions(
        self,
        interview_id: int,
        questions: list[str],
        difficulty: str,
    ) -> list[InterviewQuestion]:

        question_objects = [

            InterviewQuestion(
                interview_id=interview_id,
                question=question,
                category="General",
                difficulty=difficulty.capitalize(),
            )

            for question in questions

        ]

        self.repository.create_many(
            question_objects
        )

        return question_objects

    # =====================================================
    # Get Question
    # =====================================================

    def get_question(
        self,
        question_id: int,
    ) -> InterviewQuestion | None:

        return self.repository.get_by_id(
            question_id
        )

    # =====================================================
    # Get Interview Questions
    # =====================================================

    def get_questions(
        self,
        interview_id: int,
    ) -> list[InterviewQuestion]:

        return self.repository.get_by_interview(
            interview_id
        )

    # =====================================================
    # Get Next Question
    # =====================================================

    def get_next_question(
        self,
        interview_id: int,
        current_question_id: int,
    ) -> InterviewQuestion | None:

        return self.repository.get_next_question(
            interview_id,
            current_question_id,
        )

    # =====================================================
    # Delete Questions
    # =====================================================

    def delete_questions(
        self,
        interview_id: int,
    ) -> None:

        self.repository.delete_all(
            interview_id
        )
