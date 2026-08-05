import logging
from datetime import datetime, timezone

from app.ai.llm import get_llm


logger = logging.getLogger(__name__)


class ExecutionService:
    """
    Handles LLM execution.

    Responsibilities:
    - Sending prompts to Ollama
    - Returning generated responses
    - Logging AI executions
    """



    def __init__(
        self,
        db=None,
    ):

        self.llm = get_llm()

        self.db = db



    # =====================================================
    # Execute LLM Prompt
    # =====================================================

    def execute(
        self,
        prompt: str,
    ) -> str:


        start_time = datetime.now(
            timezone.utc
        )


        try:

            response = self.llm.invoke(
                prompt
            )


            if hasattr(
                response,
                "content"
            ):

                result = response.content

            else:

                result = str(response)



            self.log_execution(
                prompt=prompt,
                response=result,
                success=True,
            )


            return result



        except Exception as e:


            self.log_execution(
                prompt=prompt,
                response=None,
                success=False,
                error=str(e),
            )


            logger.exception(
                "LLM execution failed"
            )


            raise e



    # =====================================================
    # Execution Logger
    # =====================================================

    def log_execution(
        self,
        *,
        prompt: str,
        response: str | None = None,
        success: bool = True,
        error: str | None = None,
        prompt_name: str | None = None,
        model: str | None = None,
        user_id: int | None = None,
    ):


        try:


            logger.info(
                """
                ================================
                AI EXECUTION LOG

                Prompt Name:
                %s

                Model:
                %s

                Success:
                %s

                User:
                %s

                Error:
                %s

                ================================
                """,
                prompt_name,
                model,
                success,
                user_id,
                error,
            )


            # Future database logging
            #
            # Example:
            #
            # execution = AIExecution(
            #     prompt_name=prompt_name,
            #     model=model,
            #     input_prompt=prompt,
            #     output_response=response,
            #     success=success,
            #     error=error,
            #     user_id=user_id,
            # )
            #
            # self.db.add(execution)
            # self.db.commit()



        except Exception:


            logger.exception(
                "Failed to log AI execution"
            )
