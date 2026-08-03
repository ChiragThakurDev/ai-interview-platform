from dataclasses import dataclass
from typing import Any


@dataclass
class AIResponse:
    """
    Standard response returned by every AI provider.
    """

    success: bool

    content: Any

    model: str

    provider: str

    tokens: int | None = None

    prompt_tokens: int | None = None

    completion_tokens: int | None = None

    response_time: float | None = None

    error: str | None = None
