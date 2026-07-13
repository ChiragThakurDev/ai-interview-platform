from sqlalchemy.orm import Session

from app.repositories.dashboard_repository import (
    DashboardRepository,
)



class DashboardService:


    def __init__(
        self,
        db: Session,
    ):

        self.repository = DashboardRepository(db)



    def get_dashboard(
        self,
        user_id: int,
    ):

        reports = self.repository.get_reports(
            user_id
        )


        interviews = self.repository.get_user_interviews(
            user_id
        )


        scores = [
            report.overall_score
            for report in reports
        ]


        average_score = (
            sum(scores) / len(scores)
            if scores
            else 0
        )


        highest_score = (
            max(scores)
            if scores
            else 0
        )


        recent = []

        for interview in sorted(
            interviews,
            key=lambda x:x.created_at,
            reverse=True
        )[:5]:

            report = next(
                (
                    r
                    for r in reports
                    if r.interview_id == interview.id
                ),
                None
            )


            recent.append(
                {
                    "id": interview.id,
                    "role": interview.role,
                    "difficulty": interview.difficulty,
                    "score": (
                        report.overall_score
                        if report
                        else None
                    ),
                    "created_at": interview.created_at,
                }
            )


        return {
            "total_interviews": len(interviews),

            "average_score": round(
                average_score,
                2
            ),

            "highest_score": highest_score,

            "total_questions_answered":
                self.repository.get_answers_count(
                    user_id
                ),

            "recent_interviews": recent,
        }
