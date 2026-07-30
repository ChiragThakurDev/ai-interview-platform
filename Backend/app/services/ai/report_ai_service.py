from app.ai.factory import AIFactory
from app.ai.parser import parse_json_response

from app.ai.prompts import (
    INTERVIEW_REPORT_PROMPT,
    SKILL_ANALYSIS_PROMPT,
)

from app.schemas.ai import (
    AISkillReportResponse,
)

from app.schemas.interview_report import (
    AIInterviewReportResponse,
)


class ReportAIService:
    """
    Interview report and skill analysis service.

    Model: qwen2.5-coder:7b (via AIFactory.coding())
    Reason: Report generation is analytical reasoning over technical content.
            qwen2.5-coder produces more accurate technical assessments,
            scoring, and structured skill breakdowns than general llama models.

    Settings: temperature=0.1, json_mode=True, num_ctx=2048, keep_alive=30m
    """

    def __init__(self):
        # qwen2.5-coder:7b — precise technical analysis for reports
        self.ai = AIFactory.coding()

    # =====================================================
    # Interview Report
    # =====================================================

    def generate_interview_report(
        self,
        results: str,
    ) -> AIInterviewReportResponse:

        prompt = INTERVIEW_REPORT_PROMPT.format(
            results=results,
        )

        response = self.ai.generate(prompt)

        data = parse_json_response(response)

        # Clamp overall_score to [0, 100] — small LLMs occasionally hallucinate
        # values like 255 or -5 which crash Pydantic validation.
        if isinstance(data, dict) and "overall_score" in data:
            data["overall_score"] = max(0, min(100, int(data["overall_score"])))

        return AIInterviewReportResponse.model_validate(data)

    # =====================================================
    # Skill Report
    # =====================================================

    def generate_skill_report(
        self,
        results: str,
    ) -> AISkillReportResponse:

        prompt = SKILL_ANALYSIS_PROMPT.format(
            results=results,
        )

        response = self.ai.generate(prompt)

        data = parse_json_response(response)

        return AISkillReportResponse.model_validate(data)
