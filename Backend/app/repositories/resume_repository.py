from sqlalchemy.orm import Session

from app.models.resume import Resume


class ResumeRepository:

    def __init__(self, db: Session):
        self.db = db


    def create(self, resume: Resume):

        self.db.add(resume)
        self.db.commit()
        self.db.refresh(resume)

        return resume


    def get_by_user(self, user_id: int):

        return (
            self.db.query(Resume)
            .filter(Resume.user_id == user_id)
            .all()
        )
