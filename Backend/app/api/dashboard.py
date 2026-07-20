from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


from app.db.dependencies import get_db
from app.dependencies.auth import get_current_user

from app.models.user import User

from app.schemas.dashboard import (
    DashboardResponse,
)

from app.services.dashboard_service import (
    DashboardService,
)
from app.services.ai_service import AIService

from app.services.skill_report_service import (
    SkillReportService,
)
from app.schemas.skill_report import (
    SkillReportResponse,
)

from app.models.interview import Interview

from app.models.interview_answer import InterviewAnswer

from app.schemas.progress import (
    ProgressResponse,
)

from app.schemas.topic_analysis import (
    TopicAnalysisResponse,
)

from app.schemas.analytics import (
    AnalyticsResponse,
)


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)



@router.get(
    "",
    response_model=DashboardResponse,
)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = DashboardService(db)

    return service.get_dashboard(
        current_user.id
    )

@router.get(
    "/performance-history",
)
def get_performance_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = DashboardService(db)


    return service.get_performance_history(
        current_user.id
    )


@router.get(
    "/skills",
    response_model=SkillReportResponse,
)
def get_skill_analysis(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    skill_service = SkillReportService(db)


    existing_report = (
        skill_service.get_report(
            current_user.id
        )
    )


    if existing_report:
        return existing_report



    answers = (
        db.query(
            InterviewAnswer
        )
        .join(
            InterviewAnswer.question
        )
        .join(
            Interview
        )
        .filter(
            Interview.user_id ==
            current_user.id
        )
        .all()
    )


    if not answers:
        raise HTTPException(
            status_code=404,
            detail="No interview data found",
        )


    formatted_results = ""


    for item in answers:

        formatted_results += f"""

Question:
{item.question.question}


Answer:
{item.answer}


Score:
{item.score}


Feedback:
{item.feedback}


-----------------

"""


    ai_service = AIService()


    report = ai_service.generate_skill_report(
        formatted_results
    )


    saved_report = (
        skill_service.create_report(
            user_id=current_user.id,
            report_data=report.model_dump(),
        )
    )


    return saved_report

@router.get(
    "/progress",
    response_model=ProgressResponse,
)
def get_progress(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = DashboardService(db)

    return service.get_progress(
        current_user.id
    )



@router.get(
    "/topics",
    response_model=TopicAnalysisResponse,
)
def get_topic_analysis(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = DashboardService(db)

    return service.get_topic_analysis(
        current_user.id
    )

@router.get(
    "/analytics",
    response_model=AnalyticsResponse,
)
def get_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = DashboardService(db)

    return service.get_analytics(
        current_user.id
    )
