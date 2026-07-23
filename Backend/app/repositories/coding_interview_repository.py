from sqlalchemy.orm import Session

from app.models.coding_interview import CodingInterview
from app.models.coding_question import CodingQuestion
from app.models.coding_submission import CodingSubmission
from sqlalchemy import func
from app.models.user import User
from app.models.coding_interview import CodingInterview


class CodingInterviewRepository:


    def __init__(
            self,
            db: Session
            ):
        self.db = db



    def create(
            self,
            interview
            ):

        self.db.add(interview)
        self.db.commit()
        self.db.refresh(interview)

        return interview



    def get_by_id(
            self,
            interview_id:int
            ):

        return (
                self.db.query(CodingInterview)
                .filter(
                    CodingInterview.id == interview_id
                    )
                .first()
                )



    def get_questions(
            self,
            interview_id:int
            ):

        return (
                self.db.query(CodingQuestion)
                .filter(
                    CodingQuestion.coding_interview_id
                    ==
                    interview_id
                    )
                .all()
                )



    def create_question(
            self,
            question
            ):

        self.db.add(question)
        self.db.commit()
        self.db.refresh(question)

        return question



    def create_submission(
            self,
            submission
            ):

        self.db.add(submission)
        self.db.commit()
        self.db.refresh(submission)

        return submission



    def get_leaderboard(self):

        return (
                self.db.query(
                    User.id.label("user_id"),
                    User.name.label("user_name"),
                    func.count(CodingInterview.id).label("total_interviews"),
                    func.max(CodingInterview.score).label("best_score"),
                    func.avg(CodingInterview.score).label("average_score"),
                    )
                .join(
                    CodingInterview,
                    CodingInterview.user_id == User.id,
                    )
                .filter(
                    CodingInterview.status == "completed"
                    )
                .group_by(
                    User.id,
                    User.name,
                    )
                .order_by(
                    func.avg(CodingInterview.score).desc()
                    )
                .all()
                )


    # =====================================================
# GET USER INTERVIEW HISTORY
# =====================================================

    def get_user_interviews(
            self,
            user_id: int,
            ):

        return (
                self.db.query(CodingInterview)
                .filter(
                    CodingInterview.user_id == user_id
                    )
                .order_by(
                    CodingInterview.created_at.desc()
                    )
                .all()
                )


