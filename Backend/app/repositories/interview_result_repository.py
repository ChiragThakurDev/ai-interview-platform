from sqlalchemy.orm import Session

from app.models.interview import Interview
from app.models.interview_question import InterviewQuestion
from app.models.interview_answer import InterviewAnswer
from app.models.interview_report import InterviewReport


class InterviewResultRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    # =====================================================
    # Interview
    # =====================================================

    def get_interview(
        self,
        interview_id: int,
    ):
        return (
            self.db.query(Interview)
            .filter(
                Interview.id == interview_id
            )
            .first()
        )

    # =====================================================
    # Interview Answers
    # =====================================================

    def get_answers(
        self,
        interview_id: int,
    ):
        return (
            self.db.query(InterviewAnswer)
            .join(
                InterviewQuestion,
                InterviewAnswer.question_id == InterviewQuestion.id,
            )
            .filter(
                InterviewQuestion.interview_id == interview_id,
            )
            .all()
        )

    # =====================================================
    # Interview Report
    # =====================================================

    def get_report(
        self,
        interview_id: int,
    ):
        return (
            self.db.query(InterviewReport)
            .filter(
                InterviewReport.interview_id == interview_id
            )
            .first()
        )
