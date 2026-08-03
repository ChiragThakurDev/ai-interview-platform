"""
Prompt Renderer.

Replaces variables inside prompt templates.
"""


class PromptRenderer:

    @staticmethod
    def render(
        template: str,
        **kwargs,
    ) -> str:

        return template.format(**kwargs)
