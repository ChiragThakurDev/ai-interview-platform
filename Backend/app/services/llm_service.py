import logging
import time
from typing import Optional


from app.ai.factory import AIFactory

from app.services.prompt_service import PromptService
from app.services.prompt_execution_service import (
    PromptExecutionService,
)


logger = logging.getLogger(__name__)


class LLMService:

    def __init__(
        self,
        prompt_service: PromptService,
        execution_service: PromptExecutionService,
    ):

        self.prompt_service = prompt_service

        self.execution_service = execution_service


    # =====================================================
    # Execute Chat Prompt
    # =====================================================

    def execute_chat(
        self,
        *,
        prompt_name: str,
        variables: dict,
        user_id: Optional[int] = None,
    ) -> str:
        """
        General conversational AI execution.
        Uses AIFactory.chat()
        """

        return self._execute(
            llm=AIFactory.chat(),
            prompt_name=prompt_name,
            variables=variables,
            user_id=user_id,
        )


    # =====================================================
    # Execute JSON Prompt
    # =====================================================

    def execute_json(
        self,
        *,
        prompt_name: str,
        variables: dict,
        user_id: Optional[int] = None,
    ) -> str:
        """
        Structured JSON AI response.
        """

        return self._execute(
            llm=AIFactory.json(),
            prompt_name=prompt_name,
            variables=variables,
            user_id=user_id,
        )


    # =====================================================
    # Execute Coding Prompt
    # =====================================================

    def execute_coding(
        self,
        *,
        prompt_name: str,
        variables: dict,
        user_id: Optional[int] = None,
    ) -> str:
        """
        Coding evaluation / generation.
        """

        return self._execute(
            llm=AIFactory.coding(),
            prompt_name=prompt_name,
            variables=variables,
            user_id=user_id,
        )


    # =====================================================
    # Core Execution Engine
    # =====================================================

    def _execute(
        self,
        *,
        llm,
        prompt_name: str,
        variables: dict,
        user_id: Optional[int],
    ) -> str:


        start_time = time.perf_counter()


        prompt = None

        rendered_prompt = None


        try:

            # Get active prompt version

            prompt = (
                self.prompt_service
                .get_active_prompt(
                    prompt_name
                )
            )


            if prompt is None:

                raise ValueError(
                    f"No active prompt found: {prompt_name}"
                )


            # Render template

            rendered_prompt = (
                self.prompt_service
                .build_prompt(
                    prompt_name,
                    variables,
                )
            )


            # Execute AI

            result = llm.invoke(
                rendered_prompt
            )


            response = result.content


            latency = (
                time.perf_counter()
                -
                start_time
            )


            # Save execution log

            self.execution_service.log_execution(
                prompt=prompt,
                variables=variables,
                rendered_prompt=rendered_prompt,
                response=response,
                success=True,
                latency=latency,
                user_id=user_id,
            )


            return response



        except Exception as e:


            latency = (
                time.perf_counter()
                -
                start_time
            )


            logger.exception(
                "AI execution failed"
            )


            if prompt:

                self.execution_service.log_execution(
                    prompt=prompt,
                    variables=variables,
                    rendered_prompt=(
                        rendered_prompt or ""
                    ),
                    response=None,
                    success=False,
                    latency=latency,
                    user_id=user_id,
                    error=str(e),
                )


            raise
