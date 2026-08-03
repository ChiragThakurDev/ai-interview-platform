"""
High-level Prompt Template API.
"""

from app.ai.loader import PromptLoader
from app.ai.renderer import PromptRenderer


class PromptTemplate:

    @staticmethod
    def build(
        prompt_type: str,
        **kwargs,
    ) -> str:

        template = PromptLoader.load(prompt_type)

        return PromptRenderer.render(
            template,
            **kwargs,
        )
