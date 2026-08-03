from app.ai.factory import AIFactory
from app.ai.parser import parse_json_response
from app.ai.prompt_manager import PromptManager

from app.schemas.ai import (
    AIInterviewResponse,
)


class InterviewAIService:
    """
    Technical interview question generation service.

    Uses database-backed prompt versioning.
    """

    def __init__(self):

        self.ai = AIFactory.json()

        self.prompt_manager = PromptManager()


    def generate_questions(
        self,
        resume_text: str,
        role: str,
        difficulty: str,
        number_of_questions: int,
    ) -> AIInterviewResponse:


        prompt = self.prompt_manager.build(
            "interview_generation",
            resume=resume_text,
            role=role,
            difficulty=difficulty,
            number_of_questions=number_of_questions,
        )


        response = self.ai.generate(
            prompt
        )


        data = parse_json_response(
            response
        )


        return AIInterviewResponse.model_validate(
            data
        )
