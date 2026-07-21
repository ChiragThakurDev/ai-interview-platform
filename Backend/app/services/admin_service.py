from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.admin_repository import (
        AdminRepository,
        )


class AdminService:

    def __init__(
            self,
            db: Session,
            ):
        self.repository = AdminRepository(db)

    # =====================================================
    # Dashboard
    # =====================================================

    def get_dashboard_summary(self):

        average_score = (
                self.repository.get_average_score()
                or 0
                )

        return {
                "total_users": self.repository.get_total_users(),
                "active_users": self.repository.get_active_users(),
                "inactive_users": self.repository.get_inactive_users(),
                "total_interviews": self.repository.get_total_interviews(),
                "completed_interviews": self.repository.get_completed_interviews(),
                "pending_interviews": self.repository.get_in_progress_interviews(),
                "total_reports": self.repository.get_total_reports(),
                "average_score": round(
                    average_score,
                    2,
                    ),
                }

    # =====================================================
    # Recent Activity
    # =====================================================

    def get_recent_activity(self):

        users = self.repository.get_recent_users()

        interviews = (
                self.repository.get_recent_interviews()
                )

        reports = (
                self.repository.get_recent_reports()
                )

        return {
                "recent_users": users,
                "recent_interviews": interviews,
                "recent_reports": reports,
                }

    # =====================================================
    # Users
    # =====================================================

    def get_all_users(self):

        return self.repository.get_all_users()

    def get_user(
            self,
            user_id: int,
            ):

        user = self.repository.get_user_by_id(
                user_id
                )

        if not user:
            raise HTTPException(
                    status_code=404,
                    detail="User not found",
                    )

        return user

    def activate_user(
            self,
            user_id: int,
            ):

        user = self.get_user(user_id)

        user.is_active = True

        return self.repository.update_user(
                user
                )

    def deactivate_user(
            self,
            user_id: int,
            ):

        user = self.get_user(user_id)

        user.is_active = False

        return self.repository.update_user(
                user
                )

    def delete_user(
            self,
            user_id: int,
            ):

        user = self.get_user(user_id)

        self.repository.delete_user(
                user
                )

        return {
                "message": "User deleted successfully."
                }

    # =====================================================
    # Search + Pagination
    # =====================================================

    def search_users(
            self,
            page: int,
            limit: int,
            search: str,
            ):

        skip = (
                page - 1
                ) * limit

        users, total = (
                self.repository.search_users(
                    search=search,
                    skip=skip,
                    limit=limit,
                    )
                )

        return {
                "page": page,
                "limit": limit,
                "total": total,
                "users": users,
                }

        # =====================================================
    # Admin Analytics
    # =====================================================

    def get_analytics(self):

        return {
                "registrations":
                self.repository.get_registration_stats(),

                "interviews":
                self.repository.get_interview_stats(),

                "popular_roles":
                self.repository.get_popular_roles(),

                "difficulty_distribution":
                self.repository.get_difficulty_distribution(),

                "score_distribution":
                self.repository.get_score_distribution(),
                }
