from app.ai.factory import AIFactory
from app.ai.parser import parse_json_response
from app.ai.prompt_manager import PromptManager

from app.schemas.ai import (
    AISkillReportResponse,
)

from app.schemas.interview_report import (
    AIInterviewReportResponse,
)


class ReportAIService:
    """
    Interview report and skill analysis service.

    Uses database-backed prompt versioning.
    """

    def __init__(self):

        self.ai = AIFactory.coding()

        self.prompt_manager = PromptManager()


    # =====================================================
    # Interview Report
    # =====================================================

    def generate_interview_report(
        self,
        results: str,
    ) -> AIInterviewReportResponse:


        prompt = self.prompt_manager.build(
            "interview_report",
            results=results,
        )


        response = self.ai.generate(
            prompt
        )


        data = parse_json_response(
            response
        )


        # Clamp overall_score to [0,100]
        # LLMs can occasionally return invalid values.
        if isinstance(data, dict) and "overall_score" in data:

            data["overall_score"] = max(
                0,
                min(
                    100,
                    int(data["overall_score"])
                )
            )


        return AIInterviewReportResponse.model_validate(
            data
        )


    # =====================================================
    # Skill Report
    # =====================================================

    def generate_skill_report(
        self,
        results: str,
    ) -> AISkillReportResponse:


        prompt = self.prompt_manager.build(
            "skill_analysis",
            results=results,
        )


        response = self.ai.generate(
            prompt
        )


        data = parse_json_response(
            response
        )


        return AISkillReportResponse.model_validate(
            data
        )
