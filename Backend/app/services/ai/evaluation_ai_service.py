from app.ai.factory import AIFactory
from app.ai.parser import parse_json_response
from app.ai.prompt_manager import PromptManager

from app.schemas.ai import (
    AIAnswerEvaluationResponse,
)


class EvaluationAIService:
    """
    Interview answer evaluation AI service.

    Uses database-backed prompt versioning.
    """

    def __init__(self):

        self.ai = AIFactory.coding()

        self.prompt_manager = PromptManager()


    def evaluate_answer(
        self,
        question: str,
        answer: str,
    ) -> AIAnswerEvaluationResponse:


        prompt = self.prompt_manager.build(
            "answer_evaluation",
            question=question,
            answer=answer,
        )


        response = self.ai.generate(
            prompt
        )


        data = parse_json_response(
            response
        )


        return AIAnswerEvaluationResponse.model_validate(
            data
        )
