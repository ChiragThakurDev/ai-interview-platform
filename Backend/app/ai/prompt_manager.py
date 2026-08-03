"""
Prompt Manager.

Single entry point for all prompt generation.

Supports:
- Database backed prompts
- Static prompt fallback
- Backward compatibility
"""

from app.ai.template import PromptTemplate


class PromptManager:

    _repository = None


    def __init__(
        self,
        repository=None,
    ):
        """
        Optional repository injection.

        If repository exists:
        database prompts are used.

        Otherwise:
        fallback to static prompts.
        """

        self.repository = repository


    @classmethod
    def set_repository(
        cls,
        repository
    ):
        """
        Configure global prompt repository.
        """

        cls._repository = repository


    @staticmethod
    def build(
        prompt_type: str,
        **kwargs,
    ) -> str:
        """
        Build prompt.

        Keeps old API working.
        """

        repository = PromptManager._repository


        # Try database prompt first
        if repository:

            prompt = repository.get_active(
                prompt_type
            )

            if prompt:

                return prompt.template.format(
                    **kwargs
                )


        # Fallback to existing prompt system
        return PromptTemplate.build(
            prompt_type,
            **kwargs,
        )
