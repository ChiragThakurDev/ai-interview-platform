from app.ai.factory import AIFactory
from app.ai.parser import parse_json_response

from app.ai.prompts import (
    ANSWER_EVALUATION_PROMPT,
)

from app.schemas.ai import (
    AIAnswerEvaluationResponse,
)


class EvaluationAIService:
    """
    Interview answer evaluation AI service.

    Model: qwen2.5-coder:7b (via AIFactory.coding())
    Reason: Evaluating technical answers requires code comprehension and
            structured analysis — the same skill set as code evaluation.
            qwen2.5-coder produces more accurate scoring and feedback
            than general-purpose llama models for technical content.

    Settings: temperature=0.1, json_mode=True, num_ctx=2048, keep_alive=30m
    """

    def __init__(self):
        # qwen2.5-coder:7b — accurate at technical answer scoring
        self.ai = AIFactory.coding()

    def evaluate_answer(
        self,
        question: str,
        answer: str,
    ) -> AIAnswerEvaluationResponse:

        prompt = ANSWER_EVALUATION_PROMPT.format(
            question=question,
            answer=answer,
        )

        response = self.ai.generate(prompt)

        data = parse_json_response(response)

        return AIAnswerEvaluationResponse.model_validate(data)
