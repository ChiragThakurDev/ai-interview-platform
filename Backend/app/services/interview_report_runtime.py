from sqlalchemy.orm import Session


from app.services.interview_ai_service import (
    InterviewAIService,
)


from app.services.llm_service import (
    LLMService,
)


from app.services.prompt_service import (
    PromptService,
)


from app.services.prompt_execution_service import (
    PromptExecutionService,
)


from app.repositories.prompt_execution_repository import (
    PromptExecutionRepository,
)


from app.repositories.interview_answer_repository import (
    InterviewAnswerRepository,
)



class InterviewReportRuntime:
    """
    Generates final AI interview report.

    Flow:

    Interview Answers
            |
            v
    Prompt System
            |
            v
    LLM
            |
            v
    AI Report
    """



    def __init__(self):
        pass



    # =====================================================
    # Build AI Service
    # =====================================================

    def _get_ai_service(
        self,
        db: Session,
    ):


        prompt_service = PromptService(
            db
        )


        prompt_execution_repository = (
            PromptExecutionRepository(
                db
            )
        )


        execution_service = (
            PromptExecutionService(
                prompt_execution_repository
            )
        )


        llm_service = LLMService(

            prompt_service=prompt_service,

            execution_service=execution_service,

        )


        return InterviewAIService(

            llm_service=llm_service

        )



    # =====================================================
    # Generate Report
    # =====================================================

    def generate(
        self,
        db: Session,
        interview_id: int,
    ) -> dict:



        ai_service = self._get_ai_service(
            db
        )


        answer_repository = (
            InterviewAnswerRepository(
                db
            )
        )


        answers = (
            answer_repository
            .get_by_interview(
                interview_id
            )
        )


        if not answers:

            return {

                "overall_score":0,

                "total_questions":0,

                "report":{

                    "technical_level":"",
                    "communication":"",
                    "strengths":[],
                    "weaknesses":[],
                    "recommendation":"",
                    "summary":
                        "No answers found"

                }

            }



        payload = []

        scores = []



        for item in answers:


            scores.append(
                item.score or 0
            )


            payload.append({

                "question":
                    item.question.question,


                "category":
                    item.question.category,


                "difficulty":
                    item.question.difficulty,


                "answer":
                    item.answer,


                "score":
                    item.score,


                "feedback":
                    item.feedback,

            })



        average_score = round(

            sum(scores)
            /
            len(scores),

            2

        )



        report = (
            ai_service
            .generate_report(
                answers=payload
            )
        )



        return {


            "overall_score":
                average_score,


            "total_questions":
                len(answers),


            "report":
                report,

        }
