import os

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.dependencies.auth import get_current_user

from app.models.user import User

from app.schemas.interview import (
        GenerateInterviewRequest,
        GenerateInterviewResponse,
        InterviewListResponse,
        StartInterviewResponse,
        CurrentQuestionResponse,
        SubmitAnswerRequest,
        SubmitAnswerResponse,
        FinishInterviewResponse,
        )

from app.schemas.interview_result import (
        InterviewResultResponse,
        )

from app.schemas.interview_report import (
        InterviewReportResponse,
        )

from app.services.resume_service import ResumeService
from app.services.interview_service import InterviewService
from app.services.interview_question_service import (
        InterviewQuestionService,
        )

from app.services.interview_report_service import (
        InterviewReportService,
        )
from app.services.interview_results_service import (
    InterviewResultsService,
)

from app.services.interview_report_runtime import (
    InterviewReportRuntime,
) 


from app.services.ai_service import AIService

from app.utils.pdf import extract_text_from_pdf


router = APIRouter(
        prefix="/interview",
        tags=["Interview"],
        )


@router.post(
        "/generate/{resume_id}",
        response_model=GenerateInterviewResponse,
        )
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
            questions=[
                q.question 
                for q in ai_response.questions
                ],
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

@router.post(
        "/{interview_id}/start",
        response_model=StartInterviewResponse,
        )
def start_interview(
        interview_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
        ):

    service = InterviewService(db)

    interview = service.get_interview(interview_id)

    if interview is None:
        raise HTTPException(
                status_code=404,
                detail="Interview not found",
                )

    if interview.user_id != current_user.id:
        raise HTTPException(
                status_code=403,
                detail="Not authorized",
                )

    return service.start_interview(interview)

@router.get(
        "/{interview_id}/current-question",
        response_model=CurrentQuestionResponse,
        )
def get_current_question(
        interview_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
        ):

    service = InterviewService(db)

    interview = service.get_interview(interview_id)

    if interview is None:
        raise HTTPException(
                status_code=404,
                detail="Interview not found",
                )

    if interview.user_id != current_user.id:
        raise HTTPException(
                status_code=403,
                detail="Not authorized",
                )

    return service.get_current_question(interview)


@router.post(
    "/{interview_id}/answer",
    response_model=SubmitAnswerResponse,
)
def submit_answer(
    interview_id: int,
    request: SubmitAnswerRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    interview_service = InterviewService(db)


    interview = (
        interview_service
        .get_interview(
            interview_id
        )
    )


    if not interview:

        raise HTTPException(
            status_code=404,
            detail="Interview not found",
        )


    if interview.user_id != current_user.id:

        raise HTTPException(
            status_code=403,
            detail="Not authorized",
        )



    result = (
        interview_service
        .submit_answer(
            interview=interview,
            answer=request.answer,
        )
    )



    return result


@router.get(
    "/{interview_id}/results",
    response_model=InterviewResultResponse,
)
def get_interview_results(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    interview_service = InterviewService(db)

    interview = interview_service.get_interview(
        interview_id
    )

    if interview is None:
        raise HTTPException(
            status_code=404,
            detail="Interview not found",
        )

    if interview.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized",
        )

    results_service = InterviewResultsService(db)

    return results_service.get_results(
        interview_id
    )




@router.get(
    "/{interview_id}/report",
    response_model=InterviewReportResponse,
)
def get_interview_report(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):


    interview_service = InterviewService(db)


    interview = (
        interview_service
        .get_interview(
            interview_id
        )
    )


    if not interview:

        raise HTTPException(
            status_code=404,
            detail="Interview not found",
        )


    if interview.user_id != current_user.id:

        raise HTTPException(
            status_code=403,
            detail="Not authorized",
        )


    # ======================================
    # Generate AI Report
    # ======================================

    from app.services.interview_report_runtime import (
        InterviewReportRuntime,
    )


    runtime = InterviewReportRuntime()


    report_data = runtime.generate(
        db=db,
        interview_id=interview_id,
    )


    report_service = InterviewReportService(db)


    report = report_service.create_report(
        interview_id=interview_id,
        report_data={
            **report_data["report"],
            "overall_score": report_data["overall_score"],
        },
    )


    return report

    # ======================================
    # Generate Runtime Report
    # ======================================

    runtime = InterviewReportRuntime()


    generated_report = (
        runtime.generate(
            db=db,
            interview_id=interview_id,
        )
    )



    report_data = generated_report["report"]



    # ======================================
    # Save Report
    # ======================================

    saved_report = (
        report_service
        .create_report(
            interview_id=interview_id,
            report_data={
                "overall_score":
                    generated_report["overall_score"],

                "technical_level":
                    report_data.get(
                        "technical_level",
                        "",
                    ),

                "communication":
                    report_data.get(
                        "communication",
                        "",
                    ),

                "strengths":
                    report_data.get(
                        "strengths",
                        [],
                    ),

                "weaknesses":
                    report_data.get(
                        "weaknesses",
                        [],
                    ),

                "recommendation":
                    report_data.get(
                        "recommendation",
                        "",
                    ),

                "summary":
                    report_data.get(
                        "summary",
                        "",
                    ),
            },
        )
    )


    return saved_report


@router.post(
    "/{interview_id}/finish",
    response_model=FinishInterviewResponse,
)
def finish_interview(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = InterviewService(db)


    interview = (
        service
        .get_interview(
            interview_id
        )
    )


    if interview is None:

        raise HTTPException(
            status_code=404,
            detail="Interview not found",
        )


    if interview.user_id != current_user.id:

        raise HTTPException(
            status_code=403,
            detail="Not authorized",
        )



    # ======================================
    # Mark Interview Completed
    # ======================================

    result = (
        service
        .finish_interview(
            interview_id
        )
    )



    # ======================================
    # Generate Final AI Report
    # ======================================

    runtime = InterviewReportRuntime()


    generated_report = (
        runtime
        .generate(
            db=db,
            interview_id=interview_id,
        )
    )



    # ======================================
    # Save Report
    # ======================================

    report_service = InterviewReportService(db)


    existing_report = (
        report_service
        .get_report(
            interview_id
        )
    )



    if not existing_report:


        report_data = (
            generated_report["report"]
        )


        report_service.create_report(

            interview_id=interview_id,


            report_data={

                "overall_score":
                    generated_report[
                        "overall_score"
                    ],


                "technical_level":
                    report_data.get(
                        "technical_level",
                        "",
                    ),


                "communication":
                    report_data.get(
                        "communication",
                        "",
                    ),


                "strengths":
                    report_data.get(
                        "strengths",
                        [],
                    ),


                "weaknesses":
                    report_data.get(
                        "weaknesses",
                        [],
                    ),


                "recommendation":
                    report_data.get(
                        "recommendation",
                        "",
                    ),


                "summary":
                    report_data.get(
                        "summary",
                        "",
                    ),
            }
        )



    return result
