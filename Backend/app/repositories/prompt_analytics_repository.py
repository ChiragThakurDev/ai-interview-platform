from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.prompt_execution import PromptExecution


class PromptAnalyticsRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    # =====================================================
    # Overall Stats
    # =====================================================

    def get_stats(self):

        total = self.db.query(
            func.count(PromptExecution.id)
        ).scalar() or 0

        successful = self.db.query(
            func.count(PromptExecution.id)
        ).filter(
            PromptExecution.success.is_(True)
        ).scalar() or 0

        failed = self.db.query(
            func.count(PromptExecution.id)
        ).filter(
            PromptExecution.success.is_(False)
        ).scalar() or 0

        average_latency = self.db.query(
            func.avg(
                PromptExecution.latency
            )
        ).scalar()

        latest = (
            self.db.query(
                PromptExecution
            )
            .order_by(
                PromptExecution.created_at.desc()
            )
            .first()
        )

        success_rate = (
            (successful / total) * 100
            if total
            else 0
        )

        return {
            "total_executions": total,
            "successful": successful,
            "failed": failed,
            "success_rate": round(
                success_rate,
                2,
            ),
            "average_latency": (
                round(
                    float(average_latency),
                    3,
                )
                if average_latency is not None
                else 0
            ),
            "latest_execution": (
                latest.created_at
                if latest
                else None
            ),
        }

    # =====================================================
    # Prompt Usage
    # =====================================================

    def get_prompt_usage(self):

        return (
            self.db.query(
                PromptExecution.prompt_name,
                func.count(
                    PromptExecution.id
                ).label("count"),
            )
            .group_by(
                PromptExecution.prompt_name
            )
            .order_by(
                func.count(
                    PromptExecution.id
                ).desc()
            )
            .all()
        )

    # =====================================================
    # Model Usage
    # =====================================================

    def get_model_usage(self):

        return (
            self.db.query(
                PromptExecution.model,
                func.count(
                    PromptExecution.id
                ).label("count"),
            )
            .group_by(
                PromptExecution.model
            )
            .order_by(
                func.count(
                    PromptExecution.id
                ).desc()
            )
            .all()
        )

    # =====================================================
    # Average Latency
    # =====================================================

    def get_average_latency(self):

        return (
            self.db.query(
                PromptExecution.prompt_name,
                func.avg(
                    PromptExecution.latency
                ).label("avg_latency"),
            )
            .group_by(
                PromptExecution.prompt_name
            )
            .order_by(
                func.avg(
                    PromptExecution.latency
                ).desc()
            )
            .all()
        )

    # =====================================================
    # Failed Executions
    # =====================================================

    def get_failed_executions(
        self,
        limit: int = 100,
    ):

        return (
            self.db.query(
                PromptExecution
            )
            .filter(
                PromptExecution.success.is_(False)
            )
            .order_by(
                PromptExecution.created_at.desc()
            )
            .limit(limit)
            .all()
        )

    # =====================================================
    # Daily Usage
    # =====================================================

    def get_daily_usage(self):

        return (
            self.db.query(
                func.date(
                    PromptExecution.created_at
                ).label("day"),
                func.count(
                    PromptExecution.id
                ).label("count"),
            )
            .group_by("day")
            .order_by("day")
            .all()
        )
