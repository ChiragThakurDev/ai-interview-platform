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
            key=lambda x: x.created_at,
            reverse=True,
        )[:5]:

            report = next(
                (
                    r
                    for r in reports
                    if r.interview_id == interview.id
                ),
                None,
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
                2,
            ),
            "highest_score": highest_score,
            "total_questions_answered":
                self.repository.get_answers_count(
                    user_id
                ),
            "recent_interviews": recent,
        }

    def get_performance_history(
        self,
        user_id: int,
    ):

        results = self.repository.get_performance_history(
            user_id
        )

        history = []

        for interview, report in results:

            history.append(
                {
                    "interview_id": interview.id,
                    "role": interview.role,
                    "difficulty": interview.difficulty,
                    "score": report.overall_score,
                    "date": interview.created_at,
                }
            )

        return {
            "history": history
        }

    def get_progress(
        self,
        user_id: int,
    ):

        reports = self.repository.get_reports_by_date(
            user_id
        )

        if not reports:
            return {
                "current_score": 0,
                "previous_score": None,
                "improvement": 0,
                "trend": "no_interviews",
            }

        if len(reports) == 1:
            return {
                "current_score": reports[0].overall_score,
                "previous_score": None,
                "improvement": 0,
                "trend": "first_interview",
            }

        previous = reports[-2].overall_score
        current = reports[-1].overall_score

        improvement = current - previous

        if improvement > 0:
            trend = "improving"
        elif improvement < 0:
            trend = "declining"
        else:
            trend = "no_change"

        return {
            "current_score": current,
            "previous_score": previous,
            "improvement": improvement,
            "trend": trend,
        }

    def get_topic_analysis(
        self,
        user_id: int,
    ):

        answers = self.repository.get_all_answers(
            user_id
        )

        topics = {}

        for answer in answers:

            topic = answer.question.category

            if topic not in topics:
                topics[topic] = {
                    "total_score": 0,
                    "count": 0,
                }

            topics[topic]["total_score"] += answer.score
            topics[topic]["count"] += 1

        result = []

        for topic, data in topics.items():

            result.append(
                {
                    "topic": topic,
                    "average_score": round(
                        data["total_score"] / data["count"],
                        2,
                    ),
                    "total_questions": data["count"],
                }
            )

        result.sort(
            key=lambda x: x["average_score"],
            reverse=True,
        )

        return {
            "topics": result
        }
