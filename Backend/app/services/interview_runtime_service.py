"""
Interview Runtime Service.

Application layer between API and runtime engine.

Responsibilities:
- Manage interview state
- Evaluate answers using AI
- Save answers
- Move interview forward
"""


from app.interview_runtime.controller import InterviewController
from app.services.interview_ai_service import InterviewAIService
from app.services.interview_answer_service import InterviewAnswerService


class InterviewRuntimeService:

    def __init__(
        self,
        ai_service: InterviewAIService | None = None,
        answer_service: InterviewAnswerService | None = None,
    ):
        """
        Dependencies are optional for backward compatibility.

        Existing runtime tests:
            InterviewRuntimeService()

        Production AI flow:
            InterviewRuntimeService(
                ai_service,
                answer_service
            )
        """

        self.controller = InterviewController()

        self.ai_service = ai_service

        self.answer_service = answer_service


    # =====================================================
    # Start Interview
    # =====================================================

    def start_runtime(
        self,
        interview_id: int,
    ):

        return self.controller.start(
            interview_id
        )


    # =====================================================
    # Submit Candidate Answer
    # =====================================================

    def submit_answer(
        self,
        interview_id: int,
        score: float | None = None,
        question_id: int | None = None,
        question_text: str | None = None,
        answer: str | None = None,
        difficulty: str = "medium",
        role: str | None = None,
    ):
        """
        Supports two modes.

        --------------------------------
        Old Runtime Mode
        --------------------------------

        submit_answer(
            interview_id,
            score
        )

        Returns:
            InterviewRuntime object


        --------------------------------
        AI Evaluation Mode
        --------------------------------

        submit_answer(
            interview_id=1,
            question_id=10,
            question_text="Explain JWT",
            answer="JWT is token based authentication"
        )

        Returns:
            Evaluation response dictionary
        """


        feedback = ""

        evaluation = {}


        # =====================================================
        # AI Evaluation
        # =====================================================

        if self.ai_service and answer:

            evaluation = self.ai_service.evaluate_answer(
                question=question_text,
                answer=answer,
                difficulty=difficulty,
                role=role,
            )


            score = evaluation.get(
                "score",
                0,
            )


            feedback = evaluation.get(
                "feedback",
                "",
            )


        # =====================================================
        # Default Score
        # =====================================================

        if score is None:
            score = 0


        # =====================================================
        # Save Answer
        # =====================================================

        saved_answer = None


        if (
            self.answer_service
            and question_id
            and answer
        ):

            saved_answer = self.answer_service.create_answer(
                question_id=question_id,
                answer=answer,
                score=int(score),
                feedback=feedback,
            )


        # =====================================================
        # Update Runtime
        # =====================================================

        runtime = self.controller.submit_answer(
            interview_id,
            score,
        )


        # =====================================================
        # Backward Compatibility
        # =====================================================

        if (
            self.ai_service is None
            and self.answer_service is None
        ):
            return runtime


        # =====================================================
        # AI Response
        # =====================================================

        return {

            "answer_id": (
                saved_answer.id
                if saved_answer
                else None
            ),

            "score": score,

            "feedback": feedback,

            "strengths": evaluation.get(
                "strengths",
                [],
            ),

            "weaknesses": evaluation.get(
                "weaknesses",
                [],
            ),

            "completed": runtime.completed,

            "next_question": runtime.current_question,

        }


    # =====================================================
    # Skip Question
    # =====================================================

    def skip_question(
        self,
        interview_id: int,
    ):

        return self.controller.skip_question(
            interview_id
        )


    # =====================================================
    # Finish Interview
    # =====================================================

    def finish_runtime(
        self,
        interview_id: int,
    ):

        return self.controller.finish(
            interview_id
        )


    # =====================================================
    # Get Runtime
    # =====================================================

    def get_runtime(
        self,
        interview_id: int,
    ):

        return self.controller.get_runtime(
            interview_id
        )


    # =====================================================
    # Remove Runtime
    # =====================================================

    def remove_runtime(
        self,
        interview_id: int,
    ):

        self.controller.remove_runtime(
            interview_id
        )
