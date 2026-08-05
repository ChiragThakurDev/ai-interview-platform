from sqlalchemy.orm import Session

from app.services.transcript_aggregator import TranscriptAggregator
from app.services.evaluation_service import EvaluationService


class InterviewEvaluationRuntime:
    """
    Connects transcript system with AI evaluation.

    Flow:

    Transcript
        |
        v
    Aggregate Answer
        |
        v
    AI Evaluation
        |
        v
    Save Result
    """

    def __init__(self):

        self.aggregator = TranscriptAggregator()

        self.evaluator = EvaluationService()



    def evaluate_question(
        self,
        db: Session,
        interview_id: int,
        question_id: int,
        question: str,
    ):


        # ---------------------------------
        # Get final candidate answer
        # ---------------------------------

        answer = self.aggregator.get_answer(
            db=db,
            interview_id=interview_id,
            question_id=question_id,
        )


        if not answer:

            return {

                "success": False,

                "message": "No transcript found"

            }



        # ---------------------------------
        # AI Evaluation
        # ---------------------------------

        evaluation = self.evaluator.evaluate_answer(

            db=db,

            interview_id=interview_id,

            question_id=question_id,

            question=question,

            answer=answer,

        )



        return {

            "success": True,

            "answer": answer,

            "evaluation": {

                "id": evaluation.id,

                "score": evaluation.overall_score,

                "feedback": evaluation.feedback,

                "strengths": evaluation.strengths,

                "weaknesses": evaluation.weaknesses,

            }

        }
