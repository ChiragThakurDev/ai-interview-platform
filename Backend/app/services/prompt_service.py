from app.models.prompt import Prompt
from app.repositories.prompt_repository import PromptRepository


class PromptService:

    def __init__(
        self,
        repository: PromptRepository
    ):
        self.repository = repository


    def create_prompt(
        self,
        name: str,
        version: str,
        template: str,
        model: str = "llama3.1:8b",
        temperature: float = 0.3,
    ):

        # disable old version
        self.repository.deactivate_versions(
            name
        )

        prompt = Prompt(
            name=name,
            version=version,
            template=template,
            model=model,
            temperature=temperature,
            is_active=True,
        )

        return self.repository.create(
            prompt
        )


    def get_active_prompt(
        self,
        name: str
    ):

        return self.repository.get_active(
            name
        )


    def activate_prompt_version(
        self,
        name: str,
        version: str
    ):

        return self.repository.activate_version(
            name,
            version
        )


    def get_prompt_history(
        self,
        name: str
    ):

        return self.repository.get_all_versions(
            name
        )
