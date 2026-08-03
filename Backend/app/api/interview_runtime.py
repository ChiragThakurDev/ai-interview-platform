from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.dependencies.auth import get_current_user

from app.models.user import User

from app.ai.factory import AIFactory

from app.services.interview_ai_service import (
    InterviewAIService,
)

from app.services.interview_answer_service import (
    InterviewAnswerService,
)

from app.services.interview_runtime_service import (
    InterviewRuntimeService,
)


router = APIRouter(
    prefix="/interview-runtime",
    tags=["Interview Runtime"],
)



# =====================================================
# Dependency
# =====================================================

def get_runtime_service(
    db: Session = Depends(get_db),
):

    answer_service = InterviewAnswerService(
        db
    )


    # AI Provider

    ai_provider = AIFactory.json()


    ai_service = InterviewAIService(
        ai_provider
    )


    return InterviewRuntimeService(
        db=db,   # IMPORTANT: Enable persistent runtime
        ai_service=ai_service,
        answer_service=answer_service,
    )



# =====================================================
# Start Runtime
# =====================================================

@router.post(
    "/{interview_id}/start"
)
def start_runtime(
    interview_id: int,
    service: InterviewRuntimeService = Depends(
        get_runtime_service
    ),
    current_user: User = Depends(
        get_current_user
    ),
):

    runtime = service.start_runtime(
        interview_id
    )


    return runtime



# =====================================================
# Submit Answer
# =====================================================

@router.post(
    "/{interview_id}/answer"
)
def submit_answer(
    interview_id: int,
    question_id: int,
    question_text: str,
    answer: str,
    difficulty: str = "medium",
    role: str | None = None,

    service: InterviewRuntimeService = Depends(
        get_runtime_service
    ),

    current_user: User = Depends(
        get_current_user
    ),
):


    result = service.submit_answer(
        interview_id=interview_id,
        question_id=question_id,
        question_text=question_text,
        answer=answer,
        difficulty=difficulty,
        role=role,
    )


    return result



# =====================================================
# Skip Question
# =====================================================

@router.post(
    "/{interview_id}/skip"
)
def skip_question(
    interview_id: int,

    service: InterviewRuntimeService = Depends(
        get_runtime_service
    ),

    current_user: User = Depends(
        get_current_user
    ),
):


    return service.skip_question(
        interview_id
    )



# =====================================================
# Finish Runtime
# =====================================================

@router.post(
    "/{interview_id}/finish"
)
def finish_runtime(
    interview_id: int,

    service: InterviewRuntimeService = Depends(
        get_runtime_service
    ),

    current_user: User = Depends(
        get_current_user
    ),
):


    return service.finish_runtime(
        interview_id
    )



# =====================================================
# Get Runtime State
# =====================================================

@router.get(
    "/{interview_id}"
)
def get_runtime(
    interview_id: int,

    service: InterviewRuntimeService = Depends(
        get_runtime_service
    ),

    current_user: User = Depends(
        get_current_user
    ),
):


    runtime = service.get_runtime(
        interview_id
    )


    if runtime is None:

        raise HTTPException(
            status_code=404,
            detail="Runtime not found",
        )


    return runtime



# =====================================================
# Remove Runtime
# =====================================================

@router.delete(
    "/{interview_id}"
)
def remove_runtime(
    interview_id: int,

    service: InterviewRuntimeService = Depends(
        get_runtime_service
    ),

    current_user: User = Depends(
        get_current_user
    ),
):


    service.remove_runtime(
        interview_id
    )


    return {
        "message": "Runtime removed successfully"
    }
