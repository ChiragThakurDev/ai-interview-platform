from sqlalchemy.orm import Session

from app.models.interview_evaluation import InterviewEvaluation


class EvaluationRepository:


    def create(
        self,
        db: Session,
        interview_id: int,
        question_id: int,
        technical_score: float | None = None,
        communication_score: float | None = None,
        confidence_score: float | None = None,
        overall_score: float | None = None,
        feedback: str | None = None,
        strengths: list | None = None,
        weaknesses: list | None = None,
    ):

        evaluation = InterviewEvaluation(

            interview_id=interview_id,

            question_id=question_id,

            technical_score=technical_score,

            communication_score=communication_score,

            confidence_score=confidence_score,

            overall_score=overall_score,

            feedback=feedback,

            strengths=strengths,

            weaknesses=weaknesses,
        )


        db.add(evaluation)

        db.commit()

        db.refresh(evaluation)


        return evaluation



    def get_by_id(
        self,
        db: Session,
        evaluation_id: int,
    ):

        return (
            db.query(InterviewEvaluation)
            .filter(
                InterviewEvaluation.id == evaluation_id
            )
            .first()
        )



    def get_by_interview(
        self,
        db: Session,
        interview_id: int,
    ):

        return (
            db.query(InterviewEvaluation)
            .filter(
                InterviewEvaluation.interview_id == interview_id
            )
            .order_by(
                InterviewEvaluation.created_at.asc()
            )
            .all()
        )



    def get_by_question(
        self,
        db: Session,
        question_id: int,
    ):

        return (
            db.query(InterviewEvaluation)
            .filter(
                InterviewEvaluation.question_id == question_id
            )
            .first()
        )



    def update(
        self,
        db: Session,
        evaluation_id: int,
        **kwargs,
    ):

        evaluation = self.get_by_id(
            db,
            evaluation_id,
        )


        if not evaluation:
            return None


        for key, value in kwargs.items():

            if hasattr(
                evaluation,
                key,
            ):

                setattr(
                    evaluation,
                    key,
                    value,
                )


        db.commit()

        db.refresh(evaluation)


        return evaluation



    def delete(
        self,
        db: Session,
        evaluation_id: int,
    ):

        evaluation = self.get_by_id(
            db,
            evaluation_id,
        )


        if not evaluation:
            return False


        db.delete(
            evaluation
        )

        db.commit()


        return True
