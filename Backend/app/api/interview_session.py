from fastapi import APIRouter


from app.interview_runtime import session_manager



router = APIRouter(
    prefix="/interview-session",
    tags=["Interview Session"]
)




@router.post(
    "/{interview_id}/start"
)
def start_interview_session(
    interview_id:int,
    question_id:int = 1,
):


    session_manager.start_session(
        interview_id,
        question_id,
    )


    return {

        "success":True,

        "interview_id":
            interview_id,

        "current_question":
            question_id,

    }



@router.put(
    "/{interview_id}/question/{question_id}"
)
def update_question(
    interview_id:int,
    question_id:int,
):


    session_manager.update_question(
        interview_id,
        question_id,
    )


    return {

        "success":True,

        "current_question":
            question_id,

    }
