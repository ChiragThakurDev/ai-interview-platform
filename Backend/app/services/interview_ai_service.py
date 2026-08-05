import json
import logging

from app.services.llm_service import LLMService


logger = logging.getLogger(__name__)


class InterviewAIService:
    """
    AI brain for interview processing.

    Responsibilities:
    - Evaluate candidate answers
    - Generate scores
    - Provide feedback
    - Generate follow-up questions
    - Generate final interview reports
    """


    def __init__(
        self,
        llm_service: LLMService,
    ):
        self.llm_service = llm_service



    # =====================================================
    # Evaluate Candidate Answer
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


            result = self._parse_json(
                response
            )


            return self._normalize_evaluation(
                result
            )


        except Exception:

            logger.exception(
                "AI answer evaluation failed"
            )


            return self._default_evaluation()



    # =====================================================
    # Follow Up Question Generation
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


        try:

            return self.llm_service.execute_chat(
                prompt_name="interview_follow_up",
                variables=variables,
            )


        except Exception:

            logger.exception(
                "Follow up generation failed"
            )


            return (
                "Can you explain your approach "
                "with a practical example?"
            )



    # =====================================================
    # Final Interview Report
    # =====================================================

    def generate_report(
        self,
        *,
        answers: list[dict],
    ) -> dict:


        variables = {

            "answers": json.dumps(
                answers,
                ensure_ascii=False,
                indent=2,
            )

        }


        try:

            response = self.llm_service.execute_json(
                prompt_name="interview_final_report",
                variables=variables,
            )


            return self._parse_json(
                response
            )


        except Exception:

            logger.exception(
                "Interview report generation failed"
            )


            return {

                "overall_score": 0,

                "summary":
                    "Unable to generate report",

                "strengths": [],

                "weaknesses": [],

                "recommendation":
                    "",

            }



    # =====================================================
    # Normalize Evaluation Response
    # =====================================================

    def _normalize_evaluation(
        self,
        data: dict,
    ) -> dict:


        return {


            "score":
                self._safe_score(
                    data.get(
                        "score",
                        data.get(
                            "overall_score",
                            0
                        )
                    )
                ),


            "technical_score":
                self._safe_score(
                    data.get(
                        "technical_score",
                        0
                    )
                ),


            "communication_score":
                self._safe_score(
                    data.get(
                        "communication_score",
                        0
                    )
                ),


            "confidence_score":
                self._safe_score(
                    data.get(
                        "confidence_score",
                        0
                    )
                ),


            "feedback":
                data.get(
                    "feedback",
                    ""
                ),


            "strengths":
                data.get(
                    "strengths",
                    []
                )
                if isinstance(
                    data.get("strengths", []),
                    list
                )
                else [],


            "weaknesses":
                data.get(
                    "weaknesses",
                    []
                )
                if isinstance(
                    data.get("weaknesses", []),
                    list
                )
                else [],

        }



    # =====================================================
    # JSON Parser
    # =====================================================

    def _parse_json(
        self,
        response: str | dict,
    ) -> dict:


        if isinstance(
            response,
            dict,
        ):
            return response



        try:

            return json.loads(
                response
            )


        except json.JSONDecodeError:


            logger.warning(
                "Invalid JSON received from LLM"
            )


            return {

                "score":0,

                "feedback":response,

                "strengths":[],

                "weaknesses":[],

            }



    # =====================================================
    # Score Validator
    # =====================================================

    def _safe_score(
        self,
        value,
    ) -> float:


        try:

            score = float(
                value
            )


            if score < 0:
                return 0


            if score > 100:
                return 100


            return score


        except Exception:

            return 0



    # =====================================================
    # Default Response
    # =====================================================

    def _default_evaluation(
        self,
    ) -> dict:


        return {

            "score":0,

            "technical_score":0,

            "communication_score":0,

            "confidence_score":0,

            "feedback":
                "Unable to evaluate answer",

            "strengths":[],

            "weaknesses":[],

        }
