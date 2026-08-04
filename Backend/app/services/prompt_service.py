import logging
import time

from sqlalchemy.orm import Session

from app.ai.templates.renderer import PromptRenderer
from app.ai.llm import get_llm

from app.models.prompt import Prompt
from app.repositories.prompt_repository import PromptRepository
from app.repositories.prompt_execution_repository import PromptExecutionRepository
from app.services.prompt_execution_service import PromptExecutionService


logger = logging.getLogger(__name__)


class PromptService:

    def __init__(
        self,
        db: Session,
    ):
        self.repository = PromptRepository(db)
        self.execution_service = PromptExecutionService(
            PromptExecutionRepository(db)
        )


    # =====================================================
    # Get Active Prompt
    # =====================================================

    def get_active_prompt(
        self,
        name: str,
    ):
        return self.repository.get_active(name)



    # =====================================================
    # Build Prompt
    # =====================================================

    def build_prompt(
        self,
        name: str,
        variables: dict,
    ) -> str:

        prompt = self.repository.get_active(name)

        if prompt is None:
            raise ValueError(
                f"No active prompt found: {name}"
            )

        try:

            return PromptRenderer.render(
                prompt.template,
                **variables,
            )

        except KeyError as e:

            raise ValueError(
                f"Missing prompt variable: {e}"
            )



    # =====================================================
    # Execute Prompt
    # =====================================================

    def execute_prompt(
        self,
        name: str,
        variables: dict,
        user_id: int | None = None,
    ):

        start_time = time.time()

        prompt = self.repository.get_active(name)

        if prompt is None:
            raise ValueError(
                f"No active prompt found: {name}"
            )


        rendered_prompt = PromptRenderer.render(
            prompt.template,
            **variables,
        )


        try:

            llm = get_llm(
                model=prompt.model,
                temperature=prompt.temperature
            )


            response = llm.invoke(
                rendered_prompt
            )


            latency = int(
                (time.time() - start_time) * 1000
            )


            self.execution_service.log_execution(
                prompt=prompt,
                variables=variables,
                rendered_prompt=rendered_prompt,
                response=response.content,
                success=True,
                user_id=user_id,
                latency=latency,
            )


            return response.content



        except Exception as e:


            latency = int(
                (time.time() - start_time) * 1000
            )


            self.execution_service.log_execution(
                prompt=prompt,
                variables=variables,
                rendered_prompt=rendered_prompt,
                response=None,
                success=False,
                user_id=user_id,
                latency=latency,
                error=str(e),
            )


            logger.exception(e)

            raise



    # =====================================================
    # Create Prompt Version
    # =====================================================

    def create_prompt(
        self,
        name: str,
        version: str,
        template: str,
        provider: str = "ollama",
        model: str = "llama3.1:8b",
        temperature: float = 0.3,
        is_active: bool = False,
    ):


        if is_active:
            self.repository.deactivate_versions(name)


        prompt = Prompt(
            name=name,
            version=version,
            template=template,
            provider=provider,
            model=model,
            temperature=temperature,
            is_active=is_active,
        )


        return self.repository.create(prompt)



    # =====================================================
    # Activate Prompt Version
    # =====================================================

    def activate_prompt_version(
        self,
        name: str,
        version: str,
    ):

        return self.repository.activate_version(
            name,
            version,
        )



    # =====================================================
    # Prompt History
    # =====================================================

    def get_prompt_history(
        self,
        name: str,
    ):

        return self.repository.get_all_versions(name)



    # =====================================================
    # Delete Prompt Version
    # =====================================================

    def delete_prompt(
        self,
        name: str,
        version: str,
    ):

        prompt = self.repository.get_version(
            name,
            version,
        )


        if prompt is None:
            return None


        self.repository.delete(prompt)


        return True
