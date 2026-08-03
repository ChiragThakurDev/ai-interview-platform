import logging

from app.services.prompt_service import PromptService


logger = logging.getLogger(__name__)


class PromptLoader:
    """
    Loads prompts from database.

    Flow:

    Prompt Name
        |
        v
    PromptService
        |
        v
    Active Prompt Version
        |
        v
    Variable Injection
        |
        v
    Final Prompt
    """


    def __init__(
        self,
        prompt_service: PromptService
    ):
        self.prompt_service = prompt_service



    def load(
        self,
        name: str,
        variables: dict | None = None
    ) -> str:
        """
        Load active prompt from database
        and render variables.

        Example:

        load(
            "chat",
            {
                "name": "Chirag",
                "question": ""
            }
        )
        """


        variables = variables or {}



        # ---------------------------------
        # Fetch active prompt version
        # ---------------------------------

        prompt = self.prompt_service.get_active_prompt(
            name
        )


        if not prompt:

            logger.warning(
                "Active prompt not found: %s",
                name
            )

            raise ValueError(
                f"Active prompt not found: {name}"
            )



        if not prompt.template:

            raise ValueError(
                f"Prompt template empty: {name}"
            )



        # ---------------------------------
        # Render variables
        # ---------------------------------

        try:

            formatted_prompt = prompt.template.format(
                **variables
            )


        except KeyError as error:

            missing_variable = error.args[0]

            logger.error(
                "Missing prompt variable %s for prompt %s",
                missing_variable,
                name
            )


            raise ValueError(
                f"Missing prompt variable: {missing_variable}"
            )



        except Exception as error:

            logger.exception(
                "Prompt rendering failed: %s",
                name
            )

            raise ValueError(
                f"Prompt rendering failed: {error}"
            )



        return formatted_prompt
