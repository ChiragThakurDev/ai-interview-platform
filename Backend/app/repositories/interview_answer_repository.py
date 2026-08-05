from sqlalchemy.orm import Session, joinedload

from app.models.interview_answer import InterviewAnswer
from app.models.interview_question import InterviewQuestion


class InterviewAnswerRepository:

    def __init__(self, db: Session):
        self.db = db

    # =====================================================
    # Create
    # =====================================================

    def create(
        self,
        interview_answer: InterviewAnswer,
    ) -> InterviewAnswer:

        self.db.add(interview_answer)
        self.db.commit()
        self.db.refresh(interview_answer)

        return interview_answer

    # =====================================================
    # Get By Question
    # =====================================================

    def get_by_question(
        self,
        question_id: int,
    ) -> InterviewAnswer | None:

        return (
            self.db.query(InterviewAnswer)
            .filter(
                InterviewAnswer.question_id == question_id
            )
            .first()
        )

    # =====================================================
    # Get All Answers For Interview
    # =====================================================

    def get_by_interview(
        self,
        interview_id: int,
    ) -> list[InterviewAnswer]:

        return (
            self.db.query(InterviewAnswer)
            .join(
                InterviewQuestion,
                InterviewAnswer.question_id == InterviewQuestion.id,
            )
            .options(
                joinedload(
                    InterviewAnswer.question
                )
            )
            .filter(
                InterviewQuestion.interview_id == interview_id
            )
            .order_by(
                InterviewQuestion.id.asc()
            )
            .all()
        )

    # =====================================================
    # Update
    # =====================================================

    def update(
        self,
        interview_answer: InterviewAnswer,
        answer: str,
        score: int,
        feedback: str,
    ) -> InterviewAnswer:

        interview_answer.answer = answer
        interview_answer.score = score
        interview_answer.feedback = feedback

        self.db.commit()
        self.db.refresh(interview_answer)

        return interview_answer

    # =====================================================
    # Delete
    # =====================================================

    def delete(
        self,
        interview_answer: InterviewAnswer,
    ) -> None:

        self.db.delete(interview_answer)
        self.db.commit()
