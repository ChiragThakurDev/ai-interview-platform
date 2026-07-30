from app.ai.factory import AIFactory
from app.ai.parser import parse_json_response

from app.ai.prompts import (
    ROADMAP_PROMPT,
)

from app.schemas.roadmap import (
    LearningRoadmapResponse,
)


class RoadmapAIService:
    """
    Learning roadmap generation service.

    Model: qwen2.5-coder:7b (via AIFactory.json())
    Reason: Roadmap generation requires strict JSON schema output with
            nested weekly plans. qwen2.5-coder produces more reliable
            structured JSON than llama at this size. Zero temperature
            ensures deterministic, well-formatted roadmap output.

    Settings: temperature=0.0, json_mode=True, num_ctx=2048, keep_alive=30m
    """

    def __init__(self):
        # qwen2.5-coder:7b — reliable JSON for nested roadmap schema
        self.ai = AIFactory.json()

    # =====================================================
    # Generate Learning Roadmap
    # =====================================================

    def generate_learning_roadmap(
        self,
        skill_report: str,
    ) -> LearningRoadmapResponse:

        prompt = ROADMAP_PROMPT.format(
            skill_report=skill_report,
        )

        response = self.ai.generate(prompt)

        data = parse_json_response(response)

        return LearningRoadmapResponse.model_validate(data)
