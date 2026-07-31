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
    CHAT_MODEL,
    JSON_MODEL,
    CODING_MODEL,
    FAST_MODEL,
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


# =====================================================
# Provider Factory Functions
# =====================================================
# Called exclusively by AIFactory — do not call directly from services.


def get_chat_provider() -> OllamaProvider:
    """
    Conversational chat provider.
    Model: llama3.2:3b
    - Low temperature for coherent but natural responses.
    - Smaller ctx (2048) since chat turns are short.
    - No JSON mode — returns natural language.
    """
    return OllamaProvider(
        model=CHAT_MODEL,
        temperature=0.7,
        json_mode=False,
        num_ctx=2048,
        num_predict=512,
        keep_alive="30m",
        fallback_model="llama3.2:3b",
        timeout=45,
    )


def get_coding_provider() -> OllamaProvider:
    """
    Code generation and evaluation provider.
    Model: qwen2.5-coder:7b
    - Near-zero temperature for correct, deterministic code.
    - JSON mode on — all coding tasks return structured JSON.
    - num_predict=4096: coding questions with test cases + starter code + solutions
      can easily exceed 2000+ tokens per question. 1024 caused truncated/broken JSON.
    """
    return OllamaProvider(
        model=CODING_MODEL,
        temperature=0.1,
        json_mode=True,
        num_ctx=2048,
        num_predict=2048,
        keep_alive="30m",
        fallback_model="deepseek-coder:1.3b",
        timeout=60,
    )


def get_creative_coding_provider() -> OllamaProvider:
    """
    Code generation provider with higher temperature.
    Model: qwen2.5-coder:7b
    - Higher temperature (0.8) for varied topic generation.
    - JSON mode on.
    """
    return OllamaProvider(
        model=CODING_MODEL,
        temperature=0.8,
        json_mode=True,
        num_ctx=2048,
        num_predict=2048,
        keep_alive="30m",
        fallback_model="deepseek-coder:1.3b",
        timeout=60,
    )



def get_json_provider() -> OllamaProvider:
    """
    Structured JSON output provider.
    Model: qwen2.5-coder:7b
    - Zero temperature for fully deterministic schema-compliant output.
    - JSON mode enforced.
    - Used for question generation, resume analysis, roadmaps.
    """
    return OllamaProvider(
        model=JSON_MODEL,
        temperature=0.0,
        json_mode=True,
        num_ctx=2048,
        num_predict=1024,
        keep_alive="30m",
        fallback_model="deepseek-coder:1.3b",
        timeout=45,
    )


def get_fast_provider() -> OllamaProvider:
    """
    Low-latency general-purpose provider.
    Model: llama3.2:3b
    - Smallest model, fastest inference, fits 100% in VRAM.
    - No JSON mode — returns natural language.
    - Reduced ctx and predict for maximum speed.
    """
    return OllamaProvider(
        model=FAST_MODEL,
        temperature=0.2,
        json_mode=False,
        num_ctx=1024,
        num_predict=512,
        keep_alive="30m",
        fallback_model="deepseek-coder:1.3b",
        timeout=30,
    )
