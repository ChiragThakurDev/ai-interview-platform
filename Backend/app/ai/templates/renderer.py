"""
Prompt Template Renderer.

Responsible for injecting variables
into prompt templates.
"""

import logging


logger = logging.getLogger(__name__)


class PromptRenderer:
    """
    Render dynamic prompt templates.

    Example:

    Template:
        "Analyze resume {resume}"

    Variables:
        resume="John CV"

    Output:
        "Analyze resume John CV"
    """


    @staticmethod
    def render(
        template: str,
        **kwargs,
    ) -> str:
        """
        Replace template variables.
        """

        try:

            return template.format(
                **kwargs
            )


        except KeyError as e:

            missing_key = e.args[0]

            logger.error(
                f"Missing prompt variable: {missing_key}"
            )

            raise ValueError(
                f"Missing prompt variable: {missing_key}"
            )


        except Exception as e:

            logger.error(
                f"Prompt rendering failed: {str(e)}"
            )

            raise
