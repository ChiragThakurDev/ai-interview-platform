from fastapi import APIRouter

from app.schemas.roadmap import LearningRoadmapResponse
from app.services.roadmap_service import RoadmapService

router = APIRouter(
    prefix="/roadmap",
    tags=["Roadmap"],
)


@router.post(
    "/generate",
    response_model=LearningRoadmapResponse,
)
def generate_learning_roadmap(
    skill_report: str,
):
    """
    Generate a personalized learning roadmap
    from the candidate's skill report.
    """

    service = RoadmapService()

    return service.generate_roadmap(
        skill_report
    )
