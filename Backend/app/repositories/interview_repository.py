from sqlalchemy.orm import Session

from app.models.interview import Interview


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

    def delete(self, interview: Interview):
        self.db.delete(interview)
        self.db.commit()
