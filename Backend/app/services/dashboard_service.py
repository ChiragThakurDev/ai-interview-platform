from sqlalchemy.orm import Session

from app.repositories.dashboard_repository import DashboardRepository


class DashboardService:

    def __init__(
        self,
        db: Session,
    ):
        self.repository = DashboardRepository(db)

    # ----------------------------------
    # Dashboard Overview
    # ----------------------------------

    def get_dashboard(
        self,
        user_id: int,
    ):

        reports = self.repository.get_reports(user_id)
        interviews = self.repository.get_user_interviews(user_id)

        scores = [
            report.overall_score
            for report in reports
        ]

        average_score = (
            round(sum(scores) / len(scores), 2)
            if scores
            else 0
        )

        highest_score = (
            max(scores)
            if scores
            else 0
        )

        recent_interviews = []

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

            recent_interviews.append(
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
            "average_score": average_score,
            "highest_score": highest_score,
            "total_questions_answered": self.repository.get_answers_count(
                user_id
            ),
            "recent_interviews": recent_interviews,
        }

    # ----------------------------------
    # Performance History
    # ----------------------------------

    def get_performance_history(
        self,
        user_id: int,
    ):

        history = []

        results = self.repository.get_performance_history(
            user_id
        )

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
            "history": history,
        }

    # ----------------------------------
    # Progress
    # ----------------------------------

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

    # ----------------------------------
    # Topic Analysis
    # ----------------------------------

    def get_topic_analysis(
        self,
        user_id: int,
    ):

        answers = self.repository.get_all_answers(
            user_id
        )

        topics = {}

        for answer in answers:

            if answer.score is None:
                continue

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
            "topics": result,
        }

    # ----------------------------------
    # Analytics
    # ----------------------------------

    def get_analytics(
        self,
        user_id: int,
    ):

        reports = self.repository.get_all_reports(
            user_id
        )

        report_interviews = (
            self.repository.get_reports_with_interviews(
                user_id
            )
        )

        interviews = self.repository.get_roles(
            user_id
        )

        score_distribution = {
            "0-20": 0,
            "21-40": 0,
            "41-60": 0,
            "61-80": 0,
            "81-100": 0,
        }

        for report in reports:

            score = report.overall_score

            if score <= 20:
                score_distribution["0-20"] += 1

            elif score <= 40:
                score_distribution["21-40"] += 1

            elif score <= 60:
                score_distribution["41-60"] += 1

            elif score <= 80:
                score_distribution["61-80"] += 1

            else:
                score_distribution["81-100"] += 1

        difficulty_scores = {
            "easy": [],
            "medium": [],
            "hard": [],
        }

        for report, interview in report_interviews:

            difficulty = interview.difficulty.lower()

            if difficulty in difficulty_scores:
                difficulty_scores[difficulty].append(
                    report.overall_score
                )

        difficulty_stats = {}

        for difficulty in [
            "easy",
            "medium",
            "hard",
        ]:

            scores = difficulty_scores[difficulty]

            difficulty_stats[difficulty] = (
                round(
                    sum(scores) / len(scores),
                    2,
                )
                if scores
                else 0
            )

        role_stats = {}

        for interview in interviews:

            role = interview.role

            role_stats[role] = (
                role_stats.get(role, 0) + 1
            )

        return {
            "score_distribution": score_distribution,
            "difficulty_stats": difficulty_stats,
            "role_stats": role_stats,
        }
