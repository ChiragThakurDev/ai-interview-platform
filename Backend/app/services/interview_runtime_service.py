"""
Interview Runtime Service.

Handles complete interview runtime lifecycle.

Responsibilities:
- Start interview session
- Load runtime state
- Save answers
- Aggregate transcripts
- AI evaluation
- Update progress
- Complete interview
- Remove runtime
"""


from sqlalchemy.orm import Session


from app.interview_runtime.controller import (
    InterviewController,
)


from app.services.interview_ai_service import (
    InterviewAIService,
)


from app.services.interview_answer_service import (
    InterviewAnswerService,
)


from app.services.interview_session_service import (
    InterviewSessionService,
)


from app.services.transcript_aggregator import (
    TranscriptAggregator,
)


from app.services.evaluation_service import (
    EvaluationService,
)



class InterviewRuntimeService:



    def __init__(
        self,
        db: Session | None = None,
        ai_service: InterviewAIService | None = None,
        answer_service: InterviewAnswerService | None = None,
        evaluation_service: EvaluationService | None = None,
    ):


        self.db = db


        self.controller = InterviewController()


        self.ai_service = ai_service


        self.answer_service = answer_service


        self.evaluation_service = evaluation_service


        self.transcript_aggregator = (
            TranscriptAggregator()
        )



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



        return (
            self.controller
            .start(
                interview_id
            )
        )



    # =====================================================
    # EVALUATE TRANSCRIPT ANSWER
    # =====================================================

    def evaluate_transcript_answer(
        self,
        interview_id: int,
        question_id: int,
        question: str,
    ):


        if not self.db:

            return {
                "success":False,
                "message":"Database session missing"
            }



        answer = (
            self.transcript_aggregator
            .get_answer(
                db=self.db,
                interview_id=interview_id,
                question_id=question_id,
            )
        )



        if not answer:


            return {

                "success":False,

                "message":
                    "No transcript found"

            }



        evaluation = (

            self.evaluation_service
            .evaluate_answer(

                db=self.db,

                interview_id=interview_id,

                question_id=question_id,

                question=question,

                answer=answer,

            )

            if self.evaluation_service

            else None

        )



        return {


            "success":True,


            "answer":answer,


            "evaluation":evaluation,


        }



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



        # ===============================
        # Direct Answer Evaluation
        # ===============================

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
                0
            )


            feedback = evaluation.get(
                "feedback",
                ""
            )



        if score is None:

            score = 0



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


                    "score":score,


                    "feedback":feedback,


                    "completed":

                        session.status
                        ==
                        "completed",


                    "current_question":

                        session.current_question,


                }



        return (

            self.controller
            .submit_answer(
                interview_id,
                score,
            )

        )



    # =====================================================
    # GET RUNTIME
    # =====================================================

    def get_runtime(
        self,
        interview_id:int,
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
    # FINISH
    # =====================================================

    def finish_runtime(
        self,
        interview_id:int,
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
        interview_id:int,
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
    # REMOVE
    # =====================================================

    def remove_runtime(
        self,
        interview_id:int,
    ):


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



        return (

            self.controller
            .remove_runtime(
                interview_id
            )

        )
