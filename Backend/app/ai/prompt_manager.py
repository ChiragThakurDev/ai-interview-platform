"""
Prompt Manager.

Single entry point for all prompt generation.
"""

from app.ai.template import PromptTemplate


class PromptManager:

    @staticmethod
    def build(
        prompt_type: str,
        **kwargs,
    ) -> str:

        return PromptTemplate.build(
            prompt_type,
            **kwargs,
        )
