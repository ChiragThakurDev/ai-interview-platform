"""
Prompt Loader.

Loads prompt templates from disk.
"""

from pathlib import Path

from app.ai.version import get_prompt_version


BASE_PATH = Path(__file__).parent / "prompts"


class PromptLoader:

    @staticmethod
    def load(prompt_type: str) -> str:
        version = get_prompt_version(prompt_type)

        path = BASE_PATH / prompt_type / f"{version}.txt"

        if not path.exists():
            raise FileNotFoundError(
                f"Prompt not found: {path}"
            )

        return path.read_text(
            encoding="utf-8"
        )
