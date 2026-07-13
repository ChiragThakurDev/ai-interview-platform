from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.dependencies.auth import get_current_user

from app.models.user import User
from app.models.interview_question import InterviewQuestion

from app.schemas.interview_answer import (
    SubmitAnswerRequest,
    InterviewAnswerResponse,
)

from app.services.interview_answer_service import (
    InterviewAnswerService,
)
from app.services.ai_service import AIService


router = APIRouter(
    prefix="/answers",
    tags=["Interview Answers"],
)


@router.post(
    "/{question_id}",
    response_model=InterviewAnswerResponse,
)
def submit_answer(
    question_id: int,
    request: SubmitAnswerRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    question = (
        db.query(InterviewQuestion)
        .filter(InterviewQuestion.id == question_id)
        .first()
    )

    if not question:
        raise HTTPException(
            status_code=404,
            detail="Question not found",
        )

    ai_service = AIService()

    evaluation = ai_service.evaluate_answer(
        question=question.question,
        answer=request.answer,
    )

    score = evaluation.score
    feedback = evaluation.feedback

    answer_service = InterviewAnswerService(db)

    # Check if an answer already exists
    existing_answer = answer_service.get_answer(
        question.id
    )

    if existing_answer:
        interview_answer = answer_service.update_answer(
            interview_answer=existing_answer,
            answer=request.answer,
            score=score,
            feedback=feedback,
        )
    else:
        interview_answer = answer_service.create_answer(
            question_id=question.id,
            answer=request.answer,
            score=score,
            feedback=feedback,
        )

    return interview_answer


@router.get(
    "/{question_id}",
    response_model=InterviewAnswerResponse,
)
def get_answer(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    answer_service = InterviewAnswerService(db)

    interview_answer = answer_service.get_answer(
        question_id
    )

    if not interview_answer:
        raise HTTPException(
            status_code=404,
            detail="Answer not found",
        )

    return interview_answer
