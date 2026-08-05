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
                prompt_name="answer_evaluation",
                variables=variables,
            )


            result = self._parse_json(response)


            return self._normalize_evaluation(
                result
            )


        except Exception as e:

            logger.exception(
                f"AI answer evaluation failed: {str(e)}"
            )


            return self._default_evaluation()



    # =====================================================
    # Follow Up Question
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


        except Exception as e:

            logger.exception(
                f"Follow up generation failed: {str(e)}"
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

            "results": json.dumps(
                answers,
                ensure_ascii=False,
                indent=2,
            )

        }


        try:

            response = self.llm_service.execute_json(

                prompt_name="interview_report",

                variables=variables,

            )


            result = self._parse_json(
                response
            )


            return self._normalize_report(
                result
            )


        except Exception as e:

            logger.exception(
                f"Interview report generation failed: {str(e)}"
            )


            return self._default_report()



    # =====================================================
    # Normalize Report
    # =====================================================

    def _normalize_report(
        self,
        data: dict,
    ) -> dict:


        return {


            "overall_score":
                self._safe_score(
                    data.get(
                        "overall_score",
                        0
                    )
                ),


            "technical_level":
                data.get(
                    "technical_level",
                    ""
                ),


            "communication":
                data.get(
                    "communication",
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


            "recommendation":
                data.get(
                    "recommendation",
                    ""
                ),


            "summary":
                data.get(
                    "summary",
                    ""
                ),

        }



    # =====================================================
    # Normalize Evaluation
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
                self._ensure_list(
                    data.get(
                        "strengths",
                        []
                    )
                ),


            "weaknesses":
                self._ensure_list(
                    data.get(
                        "weaknesses",
                        []
                    )
                ),

        }



    # =====================================================
    # JSON Parser
    # =====================================================

    def _parse_json(
        self,
        response,
    ) -> dict:


        if isinstance(
            response,
            dict
        ):
            return response



        if not isinstance(
            response,
            str
        ):
            return {}



        response = response.strip()



        try:

            return json.loads(
                response
            )

        except Exception:

            pass



        if "```json" in response:


            cleaned = (

                response
                .replace(
                    "```json",
                    ""
                )
                .replace(
                    "```",
                    ""
                )
                .strip()

            )


            try:

                return json.loads(
                    cleaned
                )

            except Exception:

                pass



        logger.warning(
            "Invalid JSON returned by LLM"
        )


        return {}



    # =====================================================
    # Helpers
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



    def _ensure_list(
        self,
        value,
    ) -> list:


        if isinstance(
            value,
            list
        ):
            return value


        return []



    # =====================================================
    # Default Responses
    # =====================================================

    def _default_report(
        self,
    ) -> dict:


        return {


            "overall_score":0,


            "technical_level":"",


            "communication":"",


            "strengths":[],


            "weaknesses":[],


            "recommendation":"",


            "summary":
                "AI report generation failed",

        }



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
