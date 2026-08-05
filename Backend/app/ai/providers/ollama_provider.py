"""
Ollama Provider — Central LLM instantiation layer.

All ChatOllama instances are created HERE.

Services should NEVER directly access ChatOllama.
They should use AIFactory providers.
"""

import logging

from langchain_ollama import ChatOllama

from app.ai.models import (
    get_model,
)

from app.core.config import settings


logger = logging.getLogger(__name__)


class OllamaProvider:
    """
    Wrapper around LangChain ChatOllama.

    Provides unified interface:

    - invoke()
    - generate()
    - chat()
    - stream()
    """

    def __init__(
        self,
        model: str,
        temperature: float = 0.2,
        json_mode: bool = False,
        num_ctx: int = 2048,
        num_predict: int = 1024,
        keep_alive: str = "30m",
        fallback_model: str | None = None,
        timeout: int | None = 60,
    ):

        kwargs = {

            "model": model,

            "base_url": settings.ollama_url,

            "temperature": temperature,

            "num_ctx": num_ctx,

            "num_predict": num_predict,

            "keep_alive": keep_alive,

        }


        if timeout:

            kwargs["client_kwargs"] = {
                "timeout": timeout
            }


        if json_mode:

            kwargs["format"] = "json"



        self.llm = ChatOllama(
            **kwargs
        )


        self.model_name = model

        self.fallback_model = fallback_model

        self.kwargs = kwargs

        self.json_mode = json_mode



    # =====================================================
    # LangChain Compatible Interface
    # =====================================================

    def invoke(
        self,
        prompt: str,
    ):

        """
        Required by LLMService.

        Returns LangChain AIMessage.
        """

        return self.llm.invoke(
            prompt
        )



    # =====================================================
    # Generate Text
    # =====================================================

    def generate(
        self,
        prompt: str,
    ) -> str:


        try:

            response = self.llm.invoke(
                prompt
            )


            return response.content



        except Exception as e:


            return self._fallback(
                prompt,
                e
            )



    # =====================================================
    # Chat
    # =====================================================

    def chat(
        self,
        message,
    ) -> str:


        response = self.llm.invoke(
            message
        )


        return response.content



    # =====================================================
    # Streaming
    # =====================================================

    def stream(
        self,
        prompt:str,
    ):


        for chunk in self.llm.stream(
            prompt
        ):

            yield chunk.content



    def stream_chat(
        self,
        message,
    ):


        for chunk in self.llm.stream(
            message
        ):

            yield chunk.content



    # =====================================================
    # Fallback Model
    # =====================================================

    def _fallback(
        self,
        prompt,
        error,
    ):


        if not self.fallback_model:

            raise error



        logger.warning(
            "Primary model %s failed. "
            "Switching to %s",
            self.model_name,
            self.fallback_model,
        )



        fallback_kwargs = dict(
            self.kwargs
        )


        fallback_kwargs["model"] = (
            self.fallback_model
        )


        fallback_llm = ChatOllama(
            **fallback_kwargs
        )


        response = fallback_llm.invoke(
            prompt
        )


        return response.content





# =====================================================
# Providers
# =====================================================


def get_chat_provider():

    return OllamaProvider(

        model=get_model("chat"),

        temperature=settings.chat_temperature,

        json_mode=False,

        num_ctx=2048,

        num_predict=512,

        keep_alive="30m",

        fallback_model=get_model("fast"),

        timeout=settings.request_timeout,

    )



def get_json_provider():

    return OllamaProvider(

        model=get_model("json"),

        temperature=settings.json_temperature,

        json_mode=True,

        num_ctx=2048,

        num_predict=1024,

        keep_alive="30m",

        fallback_model=get_model("fast"),

        timeout=settings.request_timeout,

    )



def get_coding_provider():

    return OllamaProvider(

        model=get_model("coding"),

        temperature=settings.coding_temperature,

        json_mode=True,

        num_ctx=2048,

        num_predict=2048,

        keep_alive="30m",

        fallback_model=get_model("fast"),

        timeout=settings.request_timeout,

    )



def get_creative_coding_provider():

    return OllamaProvider(

        model=get_model("coding"),

        temperature=0.8,

        json_mode=True,

        num_ctx=2048,

        num_predict=2048,

        keep_alive="30m",

        fallback_model=get_model("fast"),

        timeout=settings.request_timeout,

    )



def get_fast_provider():

    return OllamaProvider(

        model=get_model("fast"),

        temperature=settings.fast_temperature,

        json_mode=False,

        num_ctx=1024,

        num_predict=512,

        keep_alive="30m",

        fallback_model=get_model("fast"),

        timeout=settings.request_timeout,

    )
