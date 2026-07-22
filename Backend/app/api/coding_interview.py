from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session


from app.db.dependencies import get_db

from app.dependencies.auth import get_current_user

from app.models.user import User


from app.services.coding_interview_service import (
    CodingInterviewService,
)


from app.schemas.coding_interview import (
    CreateCodingInterviewRequest,
    CodingInterviewResponse,
    CodingQuestionResponse,
    CreateCodingInterviewResponse,
    SubmitCodeRequest,
    SubmissionResponse,
    CodingInterviewResultResponse,
)



router = APIRouter(
    prefix="/coding-interview",
    tags=["Coding Interview"],
)



# =====================================================
# CREATE CODING INTERVIEW
# =====================================================


@router.post(
    "/create",
    response_model=CodingInterviewResponse,
)
def create_coding_interview(

    request: CreateCodingInterviewRequest,

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user),

):


    service = CodingInterviewService(
        db
    )


    interview = service.create_interview(

        user_id=current_user.id,

        role=request.role,

        company=request.company,

        language=request.language,

        difficulty=request.difficulty,

        number_of_questions=request.number_of_questions,

    )


    return interview




# =====================================================
# GET CODING INTERVIEW
# =====================================================


@router.get(
    "/{interview_id}",
    response_model=CodingInterviewResponse,
)
def get_coding_interview(

    interview_id:int,

    db:Session = Depends(get_db),

    current_user:User = Depends(get_current_user),

):


    service = CodingInterviewService(
        db
    )


    interview = service.get_interview(
        interview_id
    )


    if interview.user_id != current_user.id:

        raise HTTPException(
            status_code=403,
            detail="Not authorized",
        )


    return interview





# =====================================================
# GET QUESTIONS
# =====================================================


@router.get(
    "/{interview_id}/questions",
    response_model=list[CodingQuestionResponse],
)
def get_questions(

    interview_id:int,

    db:Session = Depends(get_db),

    current_user:User = Depends(get_current_user),

):


    service = CodingInterviewService(
        db
    )


    interview = service.get_interview(
        interview_id
    )


    if interview.user_id != current_user.id:

        raise HTTPException(
            status_code=403,
            detail="Not authorized",
        )


    return service.get_questions(
        interview_id
    )





# =====================================================
# SUBMIT CODE
# =====================================================


@router.post(
    "/submit",
    response_model=SubmissionResponse,
)
def submit_code(

    request:SubmitCodeRequest,

    db:Session = Depends(get_db),

    current_user:User = Depends(get_current_user),

):


    service = CodingInterviewService(
        db
    )


    result = service.submit_code(

        question_id=request.question_id,

        language=request.language,

        code=request.code,

    )


    return result





# =====================================================
# FINISH CODING INTERVIEW
# =====================================================


@router.post(
    "/{interview_id}/finish",
    response_model=CodingInterviewResultResponse,
)
def finish_interview(

    interview_id:int,

    db:Session = Depends(get_db),

    current_user:User = Depends(get_current_user),

):


    service = CodingInterviewService(
        db
    )


    interview = service.get_interview(
        interview_id
    )


    if interview.user_id != current_user.id:

        raise HTTPException(
            status_code=403,
            detail="Not authorized",
        )



    return service.finish_interview(
        interview_id
    )
