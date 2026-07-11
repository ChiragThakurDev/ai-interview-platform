import os

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.dependencies.auth import get_current_user

from app.models.user import User

from app.services.ai_service import AIService
from app.services.resume_service import ResumeService
from app.services.resume_analysis_service import ResumeAnalysisService

from app.utils.pdf import extract_text_from_pdf


router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.post("/analyze/{resume_id}")
def analyze_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    resume_service = ResumeService(db)

    resume = resume_service.get_resume_by_id(
        resume_id,
        current_user.id,
    )

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found",
        )

    if not os.path.exists(resume.file_path):
        raise HTTPException(
            status_code=404,
            detail="Resume file not found",
        )

    resume_text = extract_text_from_pdf(
        resume.file_path
    )

    ai_service = AIService()

    ai_result = ai_service.analyze_resume(
        resume_text
    )

    analysis_service = ResumeAnalysisService(db)

    existing = analysis_service.get_analysis(
        resume.id
    )

    if existing:
        return existing

    return analysis_service.create_analysis(
        resume.id,
        ai_result.model_dump(),
    )
