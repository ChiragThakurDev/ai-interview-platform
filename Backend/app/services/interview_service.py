from sqlalchemy.orm import Session

from app.models.interview import Interview
from app.repositories.interview_repository import InterviewRepository


class InterviewService:

    def __init__(self, db: Session):
        self.repository = InterviewRepository(db)

    def create_interview(
        self,
        user_id: int,
        resume_id: int,
        role: str,
        difficulty: str,
    ):
        interview = Interview(
            user_id=user_id,
            resume_id=resume_id,
            title=f"{role} Interview",
            role=role,
            difficulty=difficulty,
        )

        return self.repository.create(interview)

    def get_interview(self, interview_id: int):
        return self.repository.get_by_id(interview_id)

    def get_user_interviews(self, user_id: int):
        return self.repository.get_by_user(user_id)

    def delete_interview(self, interview: Interview):
        self.repository.delete(interview)
