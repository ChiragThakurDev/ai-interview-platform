from sqlalchemy.orm import Session

from app.models.resume_analysis import ResumeAnalysis
from app.repositories.resume_analysis_repository import (
    ResumeAnalysisRepository,
)


class ResumeAnalysisService:

    def __init__(self, db: Session):
        self.repository = ResumeAnalysisRepository(db)

    def create_analysis(
        self,
        resume_id: int,
        ai_result: dict,
    ):
        analysis = ResumeAnalysis(
            resume_id=resume_id,
            overall_score=ai_result["overall_score"],
            strengths=ai_result["strengths"],
            weaknesses=ai_result["weaknesses"],
            suggestions=ai_result["suggestions"],
            recommended_roles=ai_result["recommended_roles"],
            summary=ai_result["summary"],
        )

        return self.repository.create(analysis)

    def get_analysis(
        self,
        resume_id: int,
    ):
        return self.repository.get_by_resume_id(resume_id)

    def delete_analysis(
        self,
        resume_id: int,
    ):
        analysis = self.repository.get_by_resume_id(
            resume_id
        )

        if not analysis:
            return False

        self.repository.delete(analysis)
        return True
