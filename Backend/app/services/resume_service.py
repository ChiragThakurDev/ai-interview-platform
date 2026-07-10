from sqlalchemy.orm import Session

from app.models.resume import Resume
from app.repositories.resume_repository import ResumeRepository


class ResumeService:

    def __init__(self, db: Session):

        self.repository = ResumeRepository(db)


    def create_resume(
        self,
        filename,
        file_path,
        file_size,
        content_type,
        user_id
    ):

        resume = Resume(
            filename=filename,
            file_path=file_path,
            file_size=file_size,
            content_type=content_type,
            user_id=user_id,
        )

        return self.repository.create(resume)


    def get_user_resumes(self, user_id):

        return self.repository.get_by_user(user_id)
