"""
Interview Runtime Service.

Handles persistent interview runtime state.

Responsibilities:
- Start interview session
- Load existing session
- Update progress
- Save answers
- Complete interview
- Remove runtime
"""


from sqlalchemy.orm import Session

from app.interview_runtime.controller import InterviewController

from app.services.interview_ai_service import (
    InterviewAIService,
)

from app.services.interview_answer_service import (
    InterviewAnswerService,
)

from app.services.interview_session_service import (
    InterviewSessionService,
)



class InterviewRuntimeService:


    def __init__(
        self,
        db: Session | None = None,
        ai_service: InterviewAIService | None = None,
        answer_service: InterviewAnswerService | None = None,
    ):

        self.db = db

        self.controller = InterviewController()

        self.ai_service = ai_service

        self.answer_service = answer_service


        self.session_service = (
            InterviewSessionService(db)
            if db
            else None
        )



    # =====================================================
    # START RUNTIME
    # =====================================================

    def start_runtime(
        self,
        interview_id: int,
        total_questions: int = 0,
    ):


        # Persistent Database Mode

        if self.session_service:


            existing = (
                self.session_service
                .get_session(
                    interview_id
                )
            )


            if existing:
                return existing



            return (
                self.session_service
                .create_session(
                    interview_id,
                    total_questions,
                )
            )



        # Legacy Memory Mode

        return (
            self.controller
            .start(
                interview_id
            )
        )



    # =====================================================
    # SUBMIT ANSWER
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


        feedback = ""

        evaluation = {}



        # =================================================
        # AI Evaluation
        # =================================================

        if self.ai_service and answer:


            evaluation = (
                self.ai_service
                .evaluate_answer(
                    question=question_text,
                    answer=answer,
                    difficulty=difficulty,
                    role=role,
                )
            )


            score = evaluation.get(
                "score",
                0,
            )


            feedback = evaluation.get(
                "feedback",
                "",
            )



        if score is None:

            score = 0



        # =================================================
        # Save Answer
        # =================================================

        saved_answer = None


        if (
            self.answer_service
            and question_id
            and answer
        ):


            saved_answer = (
                self.answer_service
                .create_answer(
                    question_id=question_id,
                    answer=answer,
                    score=int(score),
                    feedback=feedback,
                )
            )



        # =================================================
        # Persistent Session Update
        # =================================================

        if self.session_service:


            session = (
                self.session_service
                .get_session(
                    interview_id
                )
            )


            if session:


                session = (
                    self.session_service
                    .answer_question(
                        session
                    )
                )


                return {

                    "answer_id":
                        saved_answer.id
                        if saved_answer
                        else None,


                    "score": score,


                    "feedback": feedback,


                    "completed":
                        session.status
                        == "completed",


                    "current_question":
                        session.current_question,

                }



        # =================================================
        # Legacy Runtime Mode
        # =================================================

        runtime = (
            self.controller
            .submit_answer(
                interview_id,
                score,
            )
        )


        return runtime



    # =====================================================
    # GET RUNTIME
    # =====================================================

    def get_runtime(
        self,
        interview_id: int,
    ):


        if self.session_service:


            return (
                self.session_service
                .get_session(
                    interview_id
                )
            )



        return (
            self.controller
            .get_runtime(
                interview_id
            )
        )



    # =====================================================
    # FINISH RUNTIME
    # =====================================================

    def finish_runtime(
        self,
        interview_id: int,
    ):


        if self.session_service:


            session = (
                self.session_service
                .get_session(
                    interview_id
                )
            )


            if session:


                return (
                    self.session_service
                    .finish_session(
                        session
                    )
                )



        return (
            self.controller
            .finish(
                interview_id
            )
        )



    # =====================================================
    # SKIP QUESTION
    # =====================================================

    def skip_question(
        self,
        interview_id: int,
    ):


        if self.session_service:


            session = (
                self.session_service
                .get_session(
                    interview_id
                )
            )


            if session:


                return (
                    self.session_service
                    .answer_question(
                        session
                    )
                )



        return (
            self.controller
            .skip_question(
                interview_id
            )
        )



    # =====================================================
    # REMOVE RUNTIME
    # =====================================================

    def remove_runtime(
        self,
        interview_id: int,
    ):
        """
        Remove interview runtime.

        Persistent mode:
            Deletes database session.

        Legacy mode:
            Deletes memory runtime.
        """


        # ===============================
        # Persistent Database Runtime
        # ===============================

        if self.session_service:


            session = (
                self.session_service
                .get_session(
                    interview_id
                )
            )


            if session:

                self.session_service.delete_session(
                    session
                )


            return True



        # ===============================
        # Legacy Memory Runtime
        # ===============================

        return (
            self.controller
            .remove_runtime(
                interview_id
            )
        )
