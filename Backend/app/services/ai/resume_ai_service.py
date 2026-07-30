from app.ai.parser import parse_json_response
from app.ai.prompts import RESUME_ANALYSIS_PROMPT

from app.schemas.ai import ResumeAnalysisResponse

from app.services.ai.base_ai_service import BaseAIService


class ResumeAIService(BaseAIService):

    def __init__(self):
        super().__init__()

    # =====================================================
    # Resume Analysis
    # =====================================================

    def analyze_resume(
        self,
        resume_text: str,
    ):

        prompt = RESUME_ANALYSIS_PROMPT.format(
            resume=resume_text
        )

        response = self.ai.generate(
            prompt
        )

        data = parse_json_response(
            response
        )

        return ResumeAnalysisResponse.model_validate(
            data
        )
