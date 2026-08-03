from app.ai.factory import AIFactory
from app.ai.parser import parse_json_response
from app.ai.prompt_manager import PromptManager


class CodingAIService:
    """
    Coding interview AI service.

    Uses database-backed prompt versioning.
    """

    def __init__(self):

        self.ai = AIFactory.coding()

        self.creative_ai = AIFactory.creative_coding()

        self.prompt_manager = PromptManager()


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


        prompt = self.prompt_manager.build(
            "coding_interview_generation",
            role=role,
            company=company or "Any",
            language=language,
            difficulty=difficulty,
            number_of_questions=number_of_questions,
            seed=str(uuid.uuid4()),
            previous_topics="none",
        )


        response = self.creative_ai.generate(
            prompt
        )


        return parse_json_response(
            response
        )


    # Alias for AIService compatibility
    def generate_questions(self, **kwargs):

        return self.generate_coding_questions(
            **kwargs
        )


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


        prompt = self.prompt_manager.build(
            "coding_evaluation",
            question=question,
            language=language,
            code=code,
            execution_output=execution_output,
            execution_error=execution_error,
        )


        response = self.ai.generate(
            prompt
        )


        return parse_json_response(
            response
        )


    # =====================================================
    # Coding Interview Report
    # =====================================================

    def generate_coding_report(
        self,
        results: str,
    ):


        prompt = self.prompt_manager.build(
            "coding_interview_report",
            results=results,
        )


        response = self.ai.generate(
            prompt
        )


        return parse_json_response(
            response
        )


    # Alias for AIService compatibility
    def generate_report(
        self,
        results: str
    ):

        return self.generate_coding_report(
            results
        )
