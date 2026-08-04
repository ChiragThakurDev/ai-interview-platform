import logging

from pydantic import ValidationError

from app.ai.factory import AIFactory
from app.ai.parser import parse_json_response
from app.ai.prompt_manager import PromptManager

from app.schemas.ai import (
    AISkillReportResponse,
)

from app.schemas.interview_report import (
    AIInterviewReportResponse,
)


logger = logging.getLogger(__name__)


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

        if not isinstance(data, dict):
            data = {}

        try:
            return AISkillReportResponse.model_validate(
                data
            )
        except ValidationError as error:
            logger.warning(
                "Skill report response did not match schema: %s",
                error,
            )

            return AISkillReportResponse(
                strong_skills=_as_list(
                    data.get("strong_skills")
                ),
                weak_skills=_as_list(
                    data.get("weak_skills")
                ) or [
                    "Technical communication",
                    "Problem decomposition",
                ],
                recommended_topics=_as_list(
                    data.get("recommended_topics")
                ) or [
                    "Review interview feedback",
                    "Practice targeted coding questions",
                    "Strengthen system design fundamentals",
                ],
                summary=(
                    data.get("summary")
                    if isinstance(data.get("summary"), str)
                    else (
                        "The AI response did not match the expected skill "
                        "report format, so a fallback roadmap-ready summary "
                        "was generated from the available interview data."
                    )
                ),
            )


def _as_list(value) -> list[str]:
    if isinstance(value, list):
        return [
            str(item)
            for item in value
            if str(item).strip()
        ]

    if isinstance(value, str) and value.strip():
        return [value.strip()]

    return []
