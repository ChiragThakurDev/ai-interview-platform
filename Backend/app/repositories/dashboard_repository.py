from sqlalchemy.orm import Session

from app.models.interview import Interview
from app.models.interview_report import InterviewReport
from app.models.interview_answer import InterviewAnswer


class DashboardRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def get_user_interviews(
        self,
        user_id: int,
    ):

        return (
            self.db.query(
                Interview
            )
            .filter(
                Interview.user_id == user_id
            )
            .all()
        )

    def get_reports(
        self,
        user_id: int,
    ):

        return (
            self.db.query(
                InterviewReport
            )
            .join(
                Interview
            )
            .filter(
                Interview.user_id == user_id
            )
            .all()
        )

    def get_answers_count(
        self,
        user_id: int,
    ):

        return (
            self.db.query(
                InterviewAnswer
            )
            .join(
                InterviewAnswer.question
            )
            .join(
                Interview
            )
            .filter(
                Interview.user_id == user_id
            )
            .count()
        )

    def get_performance_history(
        self,
        user_id: int,
    ):

        return (
            self.db.query(
                Interview,
                InterviewReport,
            )
            .join(
                InterviewReport,
                Interview.id == InterviewReport.interview_id,
            )
            .filter(
                Interview.user_id == user_id
            )
            .order_by(
                Interview.created_at.asc()
            )
            .all()
        )

    def get_reports_by_date(
        self,
        user_id: int,
    ):

        return (
            self.db.query(
                InterviewReport
            )
            .join(
                Interview
            )
            .filter(
                Interview.user_id == user_id
            )
            .order_by(
                Interview.created_at
            )
            .all()
        )

    def get_all_answers(
        self,
        user_id: int,
    ):

        return (
            self.db.query(
                InterviewAnswer
            )
            .join(
                InterviewAnswer.question
            )
            .join(
                Interview
            )
            .filter(
                Interview.user_id == user_id
            )
            .all()
        )

    # -----------------------------
    # Analytics Methods
    # -----------------------------

    def get_all_reports(
        self,
        user_id: int,
    ):

        return (
            self.db.query(
                InterviewReport
            )
            .join(
                Interview
            )
            .filter(
                Interview.user_id == user_id
            )
            .all()
        )

    def get_reports_with_interviews(
        self,
        user_id: int,
    ):

        return (
            self.db.query(
                InterviewReport,
                Interview,
            )
            .join(
                Interview,
                Interview.id == InterviewReport.interview_id,
            )
            .filter(
                Interview.user_id == user_id
            )
            .all()
        )

    def get_roles(
        self,
        user_id: int,
    ):

        return (
            self.db.query(
                Interview
            )
            .filter(
                Interview.user_id == user_id
            )
            .all()
        )
