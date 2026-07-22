from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.interview import Interview
from app.models.interview_report import InterviewReport


class AdminRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    # =====================================================
    # Users
    # =====================================================

    def get_total_users(self):
        return (
            self.db.query(User)
            .count()
        )

    def get_active_users(self):
        return (
            self.db.query(User)
            .filter(User.is_active == True)
            .count()
        )

    def get_inactive_users(self):
        return (
            self.db.query(User)
            .filter(User.is_active == False)
            .count()
        )

    def get_all_users(self):
        return (
            self.db.query(User)
            .order_by(User.created_at.desc())
            .all()
        )

    # =====================================================
    # Interviews
    # =====================================================

    def get_total_interviews(self):
        return (
            self.db.query(Interview)
            .count()
        )

    def get_completed_interviews(self):
        return (
            self.db.query(Interview)
            .filter(Interview.status == "completed")
            .count()
        )

    def get_in_progress_interviews(self):
        return (
            self.db.query(Interview)
            .filter(Interview.status == "in_progress")
            .count()
        )

    # =====================================================
    # Reports
    # =====================================================

    def get_total_reports(self):
        return (
            self.db.query(InterviewReport)
            .count()
        )

    def get_average_score(self):
        return (
            self.db.query(
                func.avg(InterviewReport.overall_score)
            )
            .scalar()
        )

    # =====================================================
    # Recent Activity
    # =====================================================

    def get_recent_users(
        self,
        limit: int = 10,
    ):
        return (
            self.db.query(User)
            .order_by(User.created_at.desc())
            .limit(limit)
            .all()
        )

    def get_recent_interviews(
        self,
        limit: int = 10,
    ):
        return (
            self.db.query(Interview)
            .order_by(Interview.created_at.desc())
            .limit(limit)
            .all()
        )

    def get_recent_reports(
        self,
        limit: int = 10,
    ):
        return (
            self.db.query(InterviewReport)
            .order_by(InterviewReport.created_at.desc())
            .limit(limit)
            .all()
        )

    # =====================================================
    # User Management
    # =====================================================

    def get_user_by_id(
        self,
        user_id: int,
    ):
        return (
            self.db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    def update_user(
        self,
        user: User,
    ):
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(
        self,
        user: User,
    ):
        self.db.delete(user)
        self.db.commit()

    # =====================================================
    # Search + Pagination
    # =====================================================

    def search_users(
        self,
        search: str,
        skip: int,
        limit: int,
    ):
        query = self.db.query(User)

        if search:
            query = query.filter(
                or_(
                    User.name.ilike(f"%{search}%"),
                    User.email.ilike(f"%{search}%"),
                )
            )

        total = query.count()

        users = (
            query.order_by(User.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

        return users, total

    # =====================================================
    # Admin Analytics
    # =====================================================

    def get_registration_stats(self):
        users = self.db.query(User).all()

        stats = {}

        for user in users:
            month = user.created_at.strftime("%b")
            stats[month] = stats.get(month, 0) + 1

        return stats

    def get_interview_stats(self):
        completed = (
            self.db.query(InterviewReport)
            .count()
        )

        pending = (
            self.db.query(Interview)
            .filter(Interview.status != "completed")
            .count()
        )

        return {
            "completed": completed,
            "pending": pending,
        }

    def get_popular_roles(self):
        interviews = (
            self.db.query(Interview)
            .all()
        )

        roles = {}

        for interview in interviews:
            role = interview.role
            roles[role] = roles.get(role, 0) + 1

        result = [
            {
                "role": role,
                "count": count,
            }
            for role, count in roles.items()
        ]

        result.sort(
            key=lambda x: x["count"],
            reverse=True,
        )

        return result

    def get_difficulty_distribution(self):
        interviews = (
            self.db.query(Interview)
            .all()
        )

        distribution = {
            "easy": 0,
            "medium": 0,
            "hard": 0,
        }

        for interview in interviews:
            difficulty = interview.difficulty.lower()

            if difficulty in distribution:
                distribution[difficulty] += 1

        return distribution

    def get_score_distribution(self):
        reports = (
            self.db.query(InterviewReport)
            .all()
        )

        distribution = {
            "0-20": 0,
            "21-40": 0,
            "41-60": 0,
            "61-80": 0,
            "81-100": 0,
        }

        for report in reports:
            score = report.overall_score

            if score <= 20:
                distribution["0-20"] += 1
            elif score <= 40:
                distribution["21-40"] += 1
            elif score <= 60:
                distribution["41-60"] += 1
            elif score <= 80:
                distribution["61-80"] += 1
            else:
                distribution["81-100"] += 1

        return distribution
