import json

from app.models.prompt_execution import PromptExecution
from app.repositories.prompt_execution_repository import (
    PromptExecutionRepository,
)


class PromptExecutionService:

    def __init__(
        self,
        repository: PromptExecutionRepository,
    ):
        self.repository = repository

    # =====================================================
    # Log Execution
    # =====================================================

    def log_execution(
        self,
        *,
        prompt,
        variables: dict,
        rendered_prompt: str,
        response: str | None,
        success: bool,
        latency: float | None = None,
    ):
        """
        Store one prompt execution.
        """

        execution = PromptExecution(
            prompt_id=prompt.id,
            prompt_name=prompt.name,
            prompt_version=prompt.version,
            provider=prompt.provider,
            model=prompt.model,
            variables=json.dumps(
                variables,
                ensure_ascii=False,
                default=str,
            ),
            rendered_prompt=rendered_prompt,
            response=response,
            success=success,
            latency=latency,
        )

        return self.repository.create(
            execution
        )

    # =====================================================
    # Get Logs
    # =====================================================

    def get_logs(
        self,
        limit: int = 100,
    ):
        return self.repository.get_all(
            limit
        )

    # =====================================================
    # Prompt Logs
    # =====================================================

    def get_prompt_logs(
        self,
        prompt_name: str,
        limit: int = 100,
    ):
        return self.repository.get_by_prompt(
            prompt_name,
            limit,
        )

    # =====================================================
    # Latest Log
    # =====================================================

    def latest_log(
        self,
    ):
        return self.repository.latest()
