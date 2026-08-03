from app.ai.providers.ollama_provider import (
    get_chat_provider,
    get_json_provider,
    get_coding_provider,
    get_creative_coding_provider,
    get_fast_provider,
)


class AIFactory:
    """
    Central AI Provider Factory.

    Every AI service should obtain providers ONLY from here.

    Benefits:
    - Singleton providers
    - Easy model swapping
    - Future OpenAI/Gemini support
    - Centralized configuration
    """

    _providers = {}

    @classmethod
    def _get(cls, name: str, creator):

        if name not in cls._providers:
            cls._providers[name] = creator()

        return cls._providers[name]

    @classmethod
    def chat(cls):
        return cls._get(
            "chat",
            get_chat_provider,
        )

    @classmethod
    def json(cls):
        return cls._get(
            "json",
            get_json_provider,
        )

    @classmethod
    def coding(cls):
        return cls._get(
            "coding",
            get_coding_provider,
        )

    @classmethod
    def creative_coding(cls):
        return cls._get(
            "creative_coding",
            get_creative_coding_provider,
        )

    @classmethod
    def fast(cls):
        return cls._get(
            "fast",
            get_fast_provider,
        )

    @classmethod
    def clear_cache(cls):
        """
        Useful for testing or hot-reloading.
        """

        cls._providers.clear()
