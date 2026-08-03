"""
Ollama Provider — Central LLM instantiation layer.

All ChatOllama instances are created HERE and only here.
Services must use AIFactory, not this module directly.

Performance settings rationale (RTX 2050, 4GB VRAM):
  num_ctx=2048:
    - KV cache size. 2048 tokens is enough for all interview tasks.
    - Each 1K ctx tokens ≈ ~0.5GB VRAM for 7B models at fp16.
    - Keeping ctx at 2048 prevents CPU offloading of KV cache.

  num_predict=512/1024:
    - Caps max output tokens per response.
    - Prevents runaway generation that stalls the GPU.
    - 512 is enough for chat; 1024 covers long code/report outputs.

  keep_alive="30m":
    - Keeps the model resident in VRAM between requests.
    - Eliminates the 5-15s cold-load penalty on every API call.
    - Set to 0 to free VRAM immediately after each call if needed.

  temperature:
    - 0.0 for JSON/structured: deterministic, no hallucination risk.
    - 0.1 for coding: nearly deterministic, slight creative flexibility.
    - 0.7 for chat: natural, varied conversational responses.
"""

import logging
# pyrefly: ignore [missing-import]
from langchain_ollama import ChatOllama

from app.ai.models import (
    MODEL_REGISTRY,
    get_model,
)

from app.core.config import settings

logger = logging.getLogger(__name__)

class OllamaProvider:
    """
    Wraps a ChatOllama instance with a unified generate() interface.

    Args:
        model:          Ollama model name (e.g. "llama3.2:3b")
        temperature:    Sampling temperature (0.0 = deterministic, 1.0 = creative)
        json_mode:      If True, forces Ollama to return only valid JSON output
        num_ctx:        Context window in tokens (affects VRAM usage)
        num_predict:    Max output tokens per response (prevents runaway generation)
        keep_alive:     How long to keep the model in VRAM after last request
        fallback_model: Model to use if the primary model times out or fails
        timeout:        Seconds to wait before failing and triggering fallback
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
        
        # httpx client timeout (covers connect, read, write, pool)
        if timeout:
            kwargs["client_kwargs"] = {"timeout": timeout}

        if json_mode:
            kwargs["format"] = "json"

        self.llm = ChatOllama(**kwargs)
        self.model_name = model
        self.fallback_model = fallback_model
        self.kwargs = kwargs
        self.json_mode = json_mode


    def chat(
            self,
            message,
            ) -> str:
        """
        Chat using a list of LangChain messages.
        """

        response =self.llm.invoke(messages)

        return response.content 




    def generate(self, prompt: str) -> str:
        try:
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            if self.fallback_model:
                logger.warning(
                    f"Model '{self.model_name}' failed or timed out: {e}. "
                    f"Falling back to faster model '{self.fallback_model}'..."
                )
                
                fallback_kwargs = dict(self.kwargs)
                fallback_kwargs["model"] = self.fallback_model
                if self.json_mode:
                    fallback_kwargs["format"] = "json"
                    
                fallback_llm = ChatOllama(**fallback_kwargs)
                fallback_response = fallback_llm.invoke(prompt)
                return fallback_response.content
                
            raise e


    def stream(
            self,
            prompt:str,
            ):
        """
        Stream plain text response token by token

        """
        for chunk in self.llm.stream(prompt):
            yield chunk.content

    def stream_chat(
            self,
            message,
            ):
        """
        Stream chat response token by token.

        """

        for chunk in self.llm.stream(message):
            yield chunk.content




# =====================================================
# Provider Factory Functions
# =====================================================
# Called exclusively by AIFactory — do not call directly from services.

def get_chat_provider() -> OllamaProvider:
    """
    Conversational Chat Provider
    """

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

def get_coding_provider() -> OllamaProvider:
    """
    Coding Provider
    """

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

def get_creative_coding_provider() -> OllamaProvider:
    """
    Creative Coding Provider
    """

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


def get_json_provider() -> OllamaProvider:
    """
    JSON Provider
    """

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


def get_fast_provider() -> OllamaProvider:
    """
    Fast Provider
    """

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


