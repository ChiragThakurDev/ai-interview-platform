from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.coding_interview import CodingInterview
from app.models.coding_question import CodingQuestion
from app.models.coding_submission import CodingSubmission

from app.repositories.coding_interview_repository import (
    CodingInterviewRepository,
)

from app.repositories.coding_draft_repository import (
    CodingDraftRepository,
)

from app.services.ai_service import AIService

from app.utils.code_executor import CodeExecutor



class CodingInterviewService:


    def __init__(
        self,
        db: Session
    ):

        self.db = db

        self.repository = CodingInterviewRepository(
            db
        )

        self.draft_repository = CodingDraftRepository(
            db
        )

        self.ai_service = AIService()



    # =====================================================
    # CREATE CODING INTERVIEW
    # =====================================================

    def create_interview(
        self,
        user_id: int,
        role: str,
        company: str | None,
        language: str,
        difficulty: str,
        number_of_questions: int,
    ):


        interview = CodingInterview(

            user_id=user_id,

            role=role,

            company=company,

            language=language,

            difficulty=difficulty,

            status="pending",

        )


        interview = self.repository.create(
            interview
        )


        ai_response = self.ai_service.generate_coding_questions(

            role=role,

            company=company,

            language=language,

            difficulty=difficulty,

            number_of_questions=number_of_questions,

        )


        print(
            "AI RESPONSE:",
            ai_response
        )



        for item in ai_response["questions"]:


            question = CodingQuestion(

                coding_interview_id=interview.id,

                title=item["title"],

                description=item["description"],

                starter_code=item.get(
                    "starter_code"
                ),

                solution=item.get(
                    "solution"
                ),

                difficulty=item["difficulty"],

            )


            self.repository.create_question(
                question
            )



        interview.status = "in_progress"


        interview.started_at = datetime.now(
            timezone.utc
        )


        self.db.commit()


        self.db.refresh(
            interview
        )


        return interview




    # =====================================================
    # GET INTERVIEW
    # =====================================================


    def get_interview(
        self,
        interview_id:int
    ):


        interview = self.repository.get_by_id(
            interview_id
        )


        if not interview:

            raise HTTPException(
                status_code=404,
                detail="Coding interview not found"
            )


        return interview




    # =====================================================
    # GET QUESTIONS
    # =====================================================


    def get_questions(
        self,
        interview_id:int
    ):


        return self.repository.get_questions(
            interview_id
        )



    # =====================================================
    # SUBMIT CODE
    # =====================================================

    def submit_code(
        self,
        interview_id: int,
        question_id: int,
        language: str,
        code: str,
    ):


        # ==============================
        # GET INTERVIEW
        # ==============================

        interview = (
            self.db.query(CodingInterview)
            .filter(
                CodingInterview.id == interview_id
            )
            .first()
        )


        if not interview:

            raise HTTPException(
                status_code=404,
                detail="Interview not found",
            )



        # ==============================
        # GET QUESTION
        # ==============================

        question = (
            self.db.query(CodingQuestion)
            .filter(
                CodingQuestion.id == question_id,
                CodingQuestion.coding_interview_id == interview_id
            )
            .first()
        )


        if not question:

            raise HTTPException(
                status_code=404,
                detail="Question not found for this interview",
            )



        # ==============================
        # CHECK DUPLICATE SUBMISSION
        # ==============================

        existing_submission = (
            self.db.query(CodingSubmission)
            .filter(
                CodingSubmission.question_id == question_id,
                CodingSubmission.language==language,
            )
            .first()
        )


        if existing_submission:

            raise HTTPException(
            status_code=400,
            detail="Question already submitted"
            )



        # ==============================
        # EXECUTE CODE
        # ==============================

        execution = CodeExecutor.execute_python(
            code
        )



        # ==============================
        # AI EVALUATION
        # ==============================

        result = self.ai_service.evaluate_code(

            question=question.description,

            language=language,

            code=code,

            execution_output=execution["stdout"],

            execution_error=execution["stderr"],

        )



        # ==============================
        # SAVE SUBMISSION
        # ==============================

        submission = CodingSubmission(

            question_id=question_id,

            language=language,

            code=code,

            output=(
                execution["stdout"]
                or
                execution["stderr"]
            ),

            passed=result.get(
                "passed",
                False
            ),

            score=result.get(
                "score",
                0
            ),

            feedback=result.get(
                "feedback"
            ),

        )


        self.repository.create_submission(
            submission
        )



        # ==============================
        # UPDATE INTERVIEW PROGRESS
        # ==============================


        if not existing_submission:

            interview.answered_questions += 1
            interview.current_question += 1



        total_questions = len(
            interview.questions
        )



        completed = (
            interview.answered_questions
            >=
            total_questions
        )



        next_question = None



        # ==============================
        # INTERVIEW COMPLETED
        # ==============================

        if completed:


            interview.status = "completed"


            interview.completed_at = datetime.now(
                timezone.utc
            )


            scores = []


            for q in interview.questions:


                latest = (

                    self.db.query(
                        CodingSubmission
                    )

                    .filter(
                        CodingSubmission.question_id == q.id
                    )

                    .order_by(
                        CodingSubmission.submitted_at.desc()
                    )

                    .first()

                )


                if latest:

                    scores.append(
                        latest.score or 0
                    )



            if scores:

                interview.score = (
                    sum(scores)
                    //
                    len(scores)
                )



        # ==============================
        # SEND NEXT QUESTION
        # ==============================

        else:

           next_q = interview.questions[
           interview.current_question
           ]


           next_question = {

              "id": next_q.id,

             "title": next_q.title,

             "description": next_q.description,

             "difficulty": next_q.difficulty,

            }


        self.db.commit()


        self.db.refresh(
            interview
        )



        return {


            "execution": execution,


            "evaluation": result,


            "completed": completed,


            "score": interview.score,


            "next_question": next_question,


        }
        
        
    # =====================================================
    # COMPLETE INTERVIEW
    # =====================================================

    def finish_interview(
        self,
        interview_id: int,
    ):


        interview = self.get_interview(
            interview_id
        )


        questions = interview.questions


        if not questions:

            raise HTTPException(
                status_code=400,
                detail="No questions found",
            )



        total_score = 0
        answered_questions = 0



        for question in questions:


            submission = (

                self.db.query(
                    CodingSubmission
                )

                .filter(
                    CodingSubmission.question_id == question.id
                )

                .order_by(
                    CodingSubmission.submitted_at.desc()
                )

                .first()

            )


            if submission:

                answered_questions += 1

                total_score += (
                    submission.score or 0
                )



        if answered_questions < len(questions):

            raise HTTPException(
                status_code=400,
                detail="Answer all questions before completing interview",
            )



        interview.score = (
            total_score // len(questions)
        )


        interview.status = "completed"


        interview.completed_at = datetime.now(
            timezone.utc
        )


        self.db.commit()


        self.db.refresh(
            interview
        )



        return {

            "interview_id": interview.id,

            "status": interview.status,

            "score": interview.score,

            "completed_at": interview.completed_at,

        }




    # =====================================================
    # GET INTERVIEW PROGRESS
    # =====================================================

    def get_progress(
        self,
        interview_id:int,
    ):


        interview = self.get_interview(
            interview_id
        )


        total_questions = len(
            interview.questions
        )


        answered_questions = 0

        total_score = 0



        for question in interview.questions:


            submission = (

                self.db.query(
                    CodingSubmission
                )

                .filter(
                    CodingSubmission.question_id == question.id
                )

                .order_by(
                    CodingSubmission.submitted_at.desc()
                )

                .first()

            )


            if submission:

                answered_questions += 1

                total_score += (
                    submission.score or 0
                )



        return {

            "interview_id": interview.id,

            "status": interview.status,

            "total_questions": total_questions,

            "answered_questions": answered_questions,

            "remaining_questions":
                total_questions - answered_questions,

            "current_score":
                (
                    total_score // answered_questions
                    if answered_questions
                    else 0
                ),

            "progress_percentage":
                (
                    answered_questions * 100 // total_questions
                    if total_questions
                    else 0
                ),

        }




    # =====================================================
    # GET INTERVIEW HISTORY
    # =====================================================

    def get_history(
        self,
        user_id:int,
    ):


        interviews = self.repository.get_user_interviews(
            user_id
        )


        return {

            "history": interviews

        }




    # =====================================================
    # DASHBOARD
    # =====================================================

    def get_dashboard(
        self,
        user_id:int,
    ):


        interviews = self.repository.get_user_interviews(
            user_id
        )


        total_interviews = len(
            interviews
        )


        completed_interviews = sum(

            1

            for interview in interviews

            if interview.status == "completed"

        )


        scores = [

            interview.score

            for interview in interviews

            if interview.score is not None

        ]



        return {


            "total_interviews":
                total_interviews,


            "completed_interviews":
                completed_interviews,


            "pending_interviews":
                total_interviews - completed_interviews,


            "average_score":
                (
                    sum(scores)//len(scores)
                    if scores
                    else 0
                ),


            "best_score":
                max(scores)
                if scores
                else 0,


        }




    # =====================================================
    # GENERATE REPORT
    # =====================================================

    def generate_report(
        self,
        interview_id:int,
    ):


        interview = self.get_interview(
            interview_id
        )


        result_text = ""



        for question in interview.questions:


            submission = (

                self.db.query(
                    CodingSubmission
                )

                .filter(
                    CodingSubmission.question_id == question.id
                )

                .order_by(
                    CodingSubmission.submitted_at.desc()
                )

                .first()

            )


            if not submission:

                continue



            result_text += f"""

Question:
{question.title}


Description:
{question.description}


Code:
{submission.code}


Score:
{submission.score}


Feedback:
{submission.feedback}

----------------------------

"""



        if not result_text:


            raise HTTPException(
                status_code=400,
                detail="No submissions found",
            )



        return self.ai_service.generate_coding_report(
            result_text
        )




    # =====================================================
    # LEADERBOARD
    # =====================================================

    def get_leaderboard(
        self
    ):


        rows = self.repository.get_leaderboard()



        return {


            "leaderboard":[


                {


                    "user_id": row.user_id,


                    "user_name": row.user_name,


                    "total_interviews":
                        row.total_interviews,


                    "best_score":
                        row.best_score or 0,


                    "average_score":
                        round(
                            float(row.average_score or 0),
                            2
                        ),

                }


                for row in rows


            ]

        }




    # =====================================================
    # SAVE DRAFT
    # =====================================================

    def save_draft(
        self,
        user_id:int,
        question_id:int,
        language:str,
        code:str,
    ):


        return self.draft_repository.save_draft(

            user_id=user_id,

            question_id=question_id,

            language=language,

            code=code,

        )




    # =====================================================
    # GET DRAFT
    # =====================================================

    def get_draft(
        self,
        user_id:int,
        question_id:int,
    ):


        return self.draft_repository.get_draft(

            user_id=user_id,

            question_id=question_id,

        )
