import os

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.dependencies.auth import get_current_user

from app.models.user import User

from app.schemas.interview import (GenerateInterviewRequest,GenerateInterviewResponse, InterviewListResponse,)

from app.services.resume_service import ResumeService
from app.services.interview_service import InterviewService
from app.services.interview_question_service import (
    InterviewQuestionService,
)
from app.services.ai_service import AIService

from app.utils.pdf import extract_text_from_pdf


router = APIRouter(
    prefix="/interview",
    tags=["Interview"],
)


@router.post("/generate/{resume_id}",response_model=GenerateInterviewResponse,)
def generate_interview(
    resume_id: int,
    request: GenerateInterviewRequest,
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

    ai_response = ai_service.generate_interview_questions(
        resume_text=resume_text,
        role=request.role,
        difficulty=request.difficulty,
        number_of_questions=request.number_of_questions,
    )

    interview_service = InterviewService(db)

    interview = interview_service.create_interview(
        user_id=current_user.id,
        resume_id=resume.id,
        role=request.role,
        difficulty=request.difficulty,
    )

    question_service = InterviewQuestionService(db)

    question_service.create_questions(
        interview_id=interview.id,
        questions=[q.question for q in ai_response.questions],
        difficulty=request.difficulty,
    )

    return {
        "interview": interview,
        "questions": ai_response.questions,
    }

@router.get(
    "/my",
    response_model=list[InterviewListResponse],
)
def get_my_interviews(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    interview_service = InterviewService(db)

    interviews = interview_service.get_user_interviews(
        current_user.id
    )

    return interviews
