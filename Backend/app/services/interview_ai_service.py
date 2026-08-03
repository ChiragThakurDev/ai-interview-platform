import json
import logging

from app.services.llm_service import LLMService


logger = logging.getLogger(__name__)


class InterviewAIService:
    """
    AI brain for interview evaluation.

    Responsibilities:
    - Evaluate candidate answers
    - Generate scores
    - Provide feedback
    - Suggest improvements
    """


    def __init__(
        self,
        llm_service: LLMService,
    ):
        self.llm_service = llm_service



    # =====================================================
    # Evaluate Answer
    # =====================================================

    def evaluate_answer(
        self,
        *,
        question: str,
        answer: str,
        difficulty: str = "medium",
        role: str | None = None,
    ) -> dict:


        variables = {
            "question": question,
            "answer": answer,
            "difficulty": difficulty,
            "role": role or "Software Engineer",
        }


        try:

            response = self.llm_service.execute_json(
                prompt_name="interview_answer_evaluation",
                variables=variables,
            )


            return self._parse_json(
                response
            )


        except Exception:

            logger.exception(
                "Interview answer evaluation failed"
            )

            return {
                "score": 0,
                "feedback": (
                    "Unable to evaluate answer"
                ),
                "strengths": [],
                "weaknesses": [],
            }



    # =====================================================
    # Generate Follow Up Question
    # =====================================================

    def generate_follow_up(
        self,
        *,
        question: str,
        answer: str,
    ) -> str:


        variables = {
            "question": question,
            "answer": answer,
        }


        return self.llm_service.execute_chat(
            prompt_name="interview_follow_up",
            variables=variables,
        )



    # =====================================================
    # Final Interview Report
    # =====================================================

    def generate_report(
        self,
        *,
        answers: list,
    ) -> dict:


        variables = {
            "answers": json.dumps(
                answers,
                ensure_ascii=False,
            )
        }


        response = self.llm_service.execute_json(
            prompt_name="interview_final_report",
            variables=variables,
        )


        return self._parse_json(
            response
        )



    # =====================================================
    # JSON Parser
    # =====================================================

    def _parse_json(
        self,
        response: str,
    ) -> dict:


        try:
            return json.loads(
                response
            )

        except json.JSONDecodeError:

            logger.warning(
                "Invalid JSON returned by LLM"
            )

            return {
                "score": 0,
                "feedback": response,
                "strengths": [],
                "weaknesses": [],
            }
