"""
DEPRECATED — Legacy LLM instantiation layer.

This module is kept for backward compatibility only.

New code should use:

    from app.ai.factory import AIFactory

    AIFactory.chat()
    AIFactory.coding()
    AIFactory.json()
    AIFactory.fast()

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



def _warn(name: str):

    warnings.warn(
        _DEPRECATION_MSG.format(name=name),
        DeprecationWarning,
        stacklevel=2,
    )



class AIProvider:
    """
    DEPRECATED.

    Compatibility wrapper.
    """

    def __init__(self):

        _warn("AIProvider")

        self.llm = ChatOllama(
            model=settings.json_model,
            base_url=settings.ollama_url,
            temperature=settings.json_temperature,
            format="json",
        )


    def generate(
        self,
        prompt: str,
    ) -> str:

        response = self.llm.invoke(
            [
                HumanMessage(
                    content=prompt
                )
            ]
        )

        return response.content




def get_llm():
    """
    DEPRECATED.

    Returns JSON capable LLM.
    Used by old evaluation services.
    """

    _warn("get_llm")


    return ChatOllama(

        model=settings.json_model,

        base_url=settings.ollama_url,

        temperature=settings.json_temperature,

        format="json",

    )




def get_chat_llm():
    """
    DEPRECATED.

    Returns conversational model.
    """

    _warn("get_chat_llm")


    return ChatOllama(

        model=settings.chat_model,

        base_url=settings.ollama_url,

        temperature=settings.chat_temperature,

    )




def get_coding_llm():
    """
    DEPRECATED.

    Returns coding/evaluation model.
    """

    _warn("get_coding_llm")


    return ChatOllama(

        model=settings.coding_model,

        base_url=settings.ollama_url,

        temperature=settings.coding_temperature,

    )




def get_fast_llm():
    """
    DEPRECATED.

    Returns low latency model.
    """

    _warn("get_fast_llm")


    return ChatOllama(

        model=settings.fast_model,

        base_url=settings.ollama_url,

        temperature=settings.fast_temperature,

    )




def get_ai_provider():
    """
    DEPRECATED.

    Compatibility function.
    """

    _warn("get_ai_provider")

    return AIProvider()
