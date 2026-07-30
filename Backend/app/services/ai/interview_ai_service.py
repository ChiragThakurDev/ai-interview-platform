from app.ai.factory import AIFactory
from app.ai.parser import parse_json_response

from app.ai.prompts import (
    INTERVIEW_GENERATION_PROMPT,
)

from app.schemas.ai import (
    AIInterviewResponse,
)


class InterviewAIService:
    """
    Technical interview question generation service.

    Model: qwen2.5-coder:7b (via AIFactory.json())
    Reason: Question generation requires strict JSON schema adherence.
            qwen2.5-coder follows JSON output formats more reliably than
            llama at this parameter size, producing fewer malformed responses.

    Settings: temperature=0.0, json_mode=True, num_ctx=2048, keep_alive=30m
    """

    def __init__(self):
        # qwen2.5-coder:7b — strict JSON output for question schema
        self.ai = AIFactory.json()

    def generate_questions(
        self,
        resume_text: str,
        role: str,
        difficulty: str,
        number_of_questions: int,
    ) -> AIInterviewResponse:

        prompt = INTERVIEW_GENERATION_PROMPT.format(
            resume=resume_text,
            role=role,
            difficulty=difficulty,
            number_of_questions=number_of_questions,
        )

        response = self.ai.generate(prompt)

        data = parse_json_response(response)

        return AIInterviewResponse.model_validate(data)
