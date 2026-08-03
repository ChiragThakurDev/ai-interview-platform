import json
import logging
from typing import Optional, Any

from app.models.prompt_execution import PromptExecution
from app.repositories.prompt_execution_repository import (
    PromptExecutionRepository,
)


logger = logging.getLogger(__name__)


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
        response: Optional[str],
        success: bool,
        latency: Optional[float] = None,
        user_id: Optional[int] = None,
        error: Optional[str] = None,
        tokens_used: Optional[int] = None,
    ) -> PromptExecution:
        """
        Store prompt execution details.
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


            user_id=user_id,


            error=error,


            tokens_used=tokens_used,
        )


        logger.info(
            "Prompt execution logged: %s v%s success=%s",
            prompt.name,
            prompt.version,
            success,
        )


        return self.repository.create(
            execution
        )



    # =====================================================
    # Get All Logs
    # =====================================================

    def get_logs(
        self,
        limit: int = 100,
    ):

        return self.repository.get_all(
            limit
        )



    # =====================================================
    # Get Prompt Specific Logs
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
    # Latest Execution
    # =====================================================

    def latest_log(
        self,
    ):

        return self.repository.latest()



    # =====================================================
    # Execution Metrics
    # =====================================================

    def get_metrics(
        self,
        prompt_name: Optional[str] = None,
    ):

        return self.repository.get_metrics(
            prompt_name
        )
