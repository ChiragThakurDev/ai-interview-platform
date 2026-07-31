from app.ai.factory import AIFactory
from app.ai.parser import parse_json_response

from app.ai.prompts import (
    CODING_INTERVIEW_GENERATION_PROMPT,
    CODING_EVALUATION_PROMPT,
    CODING_INTERVIEW_REPORT_PROMPT,
)


class CodingAIService:
    """
    Coding interview AI service.

    Model: qwen2.5-coder:7b (via AIFactory.coding())
    Reason: Code generation, evaluation, and analysis is this model's
            primary training objective. Significantly more accurate on
            code tasks than llama3.1:8b.

    Settings: temperature=0.1, json_mode=True, num_ctx=2048, keep_alive=30m
    """

    def __init__(self):
        # qwen2.5-coder:7b — specialist for code generation and analysis
        self.ai = AIFactory.coding()
        self.creative_ai = AIFactory.creative_coding()

    # =====================================================
    # Generate Coding Questions
    # =====================================================

    def generate_coding_questions(
        self,
        role: str,
        company: str | None,
        language: str,
        difficulty: str,
        number_of_questions: int,
    ):
        import uuid
        prompt = CODING_INTERVIEW_GENERATION_PROMPT.format(
            role=role,
            company=company or "Any",
            language=language,
            difficulty=difficulty,
            number_of_questions=number_of_questions,
            seed=str(uuid.uuid4()),
            previous_topics="none",
        )

        response = self.creative_ai.generate(prompt)

        return parse_json_response(response)

    # Alias for AIService compatibility
    def generate_questions(self, **kwargs):
        return self.generate_coding_questions(**kwargs)

    # =====================================================
    # Evaluate Code
    # =====================================================

    def evaluate_code(
        self,
        question: str,
        language: str,
        code: str,
        execution_output: str,
        execution_error: str,
    ):
        prompt = CODING_EVALUATION_PROMPT.format(
            question=question,
            language=language,
            code=code,
            execution_output=execution_output,
            execution_error=execution_error,
        )

        response = self.ai.generate(prompt)

        return parse_json_response(response)

    # =====================================================
    # Coding Interview Report
    # =====================================================

    def generate_coding_report(
        self,
        results: str,
    ):
        prompt = CODING_INTERVIEW_REPORT_PROMPT.format(
            results=results,
        )

        response = self.ai.generate(prompt)

        return parse_json_response(response)

    # Alias for AIService compatibility
    def generate_report(self, results: str):
        return self.generate_coding_report(results)
