from sqlalchemy.orm import Session

from app.models.interview_question import InterviewQuestion


class InterviewQuestionRepository:

    def __init__(self, db: Session):
        self.db = db

    # =====================================================
    # Create Questions
    # =====================================================

    def create_many(
        self,
        questions: list[InterviewQuestion],
    ) -> None:

        self.db.add_all(questions)
        self.db.commit()

    # =====================================================
    # Get Question By ID
    # =====================================================

    def get_by_id(
        self,
        question_id: int,
    ) -> InterviewQuestion | None:

        return (
            self.db.query(InterviewQuestion)
            .filter(
                InterviewQuestion.id == question_id
            )
            .first()
        )

    # =====================================================
    # Get All Questions For Interview
    # =====================================================

    def get_by_interview(
        self,
        interview_id: int,
    ) -> list[InterviewQuestion]:

        return (
            self.db.query(InterviewQuestion)
            .filter(
                InterviewQuestion.interview_id == interview_id
            )
            .order_by(
                InterviewQuestion.id.asc()
            )
            .all()
        )

    # =====================================================
    # Get Next Question
    # =====================================================

    def get_next_question(
        self,
        interview_id: int,
        current_question_id: int,
    ) -> InterviewQuestion | None:

        return (
            self.db.query(InterviewQuestion)
            .filter(
                InterviewQuestion.interview_id == interview_id,
                InterviewQuestion.id > current_question_id,
            )
            .order_by(
                InterviewQuestion.id.asc()
            )
            .first()
        )

    # =====================================================
    # Delete Questions
    # =====================================================

    def delete_all(
        self,
        interview_id: int,
    ) -> None:

        (
            self.db.query(InterviewQuestion)
            .filter(
                InterviewQuestion.interview_id == interview_id
            )
            .delete()
        )

        self.db.commit()
