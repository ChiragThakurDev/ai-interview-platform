"""
DEPRECATED — Legacy LLM instantiation layer.

This module is kept for backward compatibility only.
Do NOT use these functions in new code.

Use AIFactory instead:
    from app.ai.factory import AIFactory

    AIFactory.chat()   → llama3.2:3b  (conversational)
    AIFactory.coding() → qwen2.5-coder:7b (code generation/evaluation)
    AIFactory.json()   → qwen2.5-coder:7b (structured JSON output)
    AIFactory.fast()   → llama3.2:3b  (low-latency general tasks)
"""

import warnings
import logging

from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama

from app.core.config import settings


logger = logging.getLogger(__name__)


_DEPRECATION_MSG = (
    "{name}() is deprecated. "
    "Use AIFactory.chat() / AIFactory.json() / AIFactory.coding() instead. "
    "See app/ai/factory.py"
)


class AIProvider:
    """
    DEPRECATED — Use AIFactory + OllamaProvider instead.
    """

    def __init__(self):

        warnings.warn(
            _DEPRECATION_MSG.format(name="AIProvider"),
            DeprecationWarning,
            stacklevel=2,
        )

        self.llm = ChatOllama(
            model=settings.ollama_model,
            base_url=settings.ollama_url,
            temperature=0.1,
            format="json"
        )

    def generate(self, prompt: str) -> str:
        response = self.llm.invoke(
            [HumanMessage(content=prompt)]
        )
        return response.content


def get_llm():
    """DEPRECATED — Use AIFactory.json() or AIFactory.coding() instead."""
    warnings.warn(
        _DEPRECATION_MSG.format(name="get_llm"),
        DeprecationWarning,
        stacklevel=2,
    )
    return ChatOllama(
        model=settings.ollama_model,
        base_url=settings.ollama_url,
        temperature=0.1,
        format="json"
    )


def get_chat_llm():
    """DEPRECATED — Use AIFactory.chat() instead."""
    warnings.warn(
        _DEPRECATION_MSG.format(name="get_chat_llm"),
        DeprecationWarning,
        stacklevel=2,
    )
    return ChatOllama(
        model=settings.ollama_model,
        base_url=settings.ollama_url,
        temperature=0.7,
    )


def get_ai_provider():
    """DEPRECATED — Use AIFactory.json() or AIFactory.coding() instead."""
    warnings.warn(
        _DEPRECATION_MSG.format(name="get_ai_provider"),
        DeprecationWarning,
        stacklevel=2,
    )
    return AIProvider()
