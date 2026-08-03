from app.repositories.prompt_analytics_repository import (
    PromptAnalyticsRepository,
)


class PromptAnalyticsService:

    def __init__(
        self,
        repository: PromptAnalyticsRepository,
    ):
        self.repository = repository

    # =====================================================
    # Overall Statistics
    # =====================================================

    def get_stats(self):
        return self.repository.get_stats()

    # =====================================================
    # Prompt Usage
    # =====================================================

    def get_prompt_usage(self):
        return self.repository.get_prompt_usage()

    # =====================================================
    # Model Usage
    # =====================================================

    def get_model_usage(self):
        return self.repository.get_model_usage()

    # =====================================================
    # Average Latency
    # =====================================================

    def get_average_latency(self):
        return self.repository.get_average_latency()

    # =====================================================
    # Failed Executions
    # =====================================================

    def get_failed_executions(
        self,
        limit: int = 100,
    ):
        return self.repository.get_failed_executions(
            limit
        )

    # =====================================================
    # Daily Usage
    # =====================================================

    def get_daily_usage(self):
        return self.repository.get_daily_usage()
