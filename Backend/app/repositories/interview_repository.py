from sqlalchemy.orm import Session, joinedload

from app.models.interview import Interview
from app.models.interview_question import InterviewQuestion


class InterviewRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, interview: Interview):
        self.db.add(interview)
        self.db.commit()
        self.db.refresh(interview)
        return interview

    def get_by_id(self, interview_id: int):
        return (
            self.db.query(Interview)
            .filter(Interview.id == interview_id)
            .first()
        )

    def get_by_user(self, user_id: int):
        return (
            self.db.query(Interview)
            .filter(Interview.user_id == user_id)
            .all()
        )

    def get_with_results(
        self,
        interview_id: int,
    ):
        return (
            self.db.query(Interview)
            .options(
                joinedload(Interview.questions).joinedload(
                    InterviewQuestion.answer
                )
            )
            .filter(Interview.id == interview_id)
            .first()
        )

    def update(self, interview: Interview):
        self.db.commit()
        self.db.refresh(interview)
        return interview

    def save(self):
        self.db.commit()

    def delete(self, interview: Interview):
        self.db.delete(interview)
        self.db.commit()
