from app.ai.factory import AIFactory
from app.ai.parser import parse_json_response
from app.ai.prompt_manager import PromptManager

from app.schemas.roadmap import (
    LearningRoadmapResponse,
)


class RoadmapAIService:
    """
    Learning roadmap generation service.

    Uses database-backed prompt versioning.
    """

    def __init__(self):

        self.ai = AIFactory.json()

        self.prompt_manager = PromptManager()


    # =====================================================
    # Generate Learning Roadmap
    # =====================================================

    def generate_learning_roadmap(
        self,
        skill_report: str,
    ) -> LearningRoadmapResponse:


        prompt = self.prompt_manager.build(
            "roadmap",
            skill_report=skill_report,
        )


        response = self.ai.generate(
            prompt
        )


        data = parse_json_response(
            response
        )


        return LearningRoadmapResponse.model_validate(
            data
        )
