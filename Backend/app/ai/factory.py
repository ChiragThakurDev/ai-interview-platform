from app.ai.providers.ollama_provider import (
    get_chat_provider,
    get_json_provider,
    get_coding_provider,
    get_fast_provider,
)


class AIFactory:
    """
    Central AI Provider Factory.
    Returns shared provider instances.
    """

    _chat = None
    _json = None
    _coding = None
    _fast = None

    @classmethod
    def chat(cls):

        if cls._chat is None:
            cls._chat = get_chat_provider()

        return cls._chat

    @classmethod
    def json(cls):

        if cls._json is None:
            cls._json = get_json_provider()

        return cls._json

    @classmethod
    def coding(cls):

        if cls._coding is None:
            cls._coding = get_coding_provider()

        return cls._coding

    @classmethod
    def fast(cls):

        if cls._fast is None:
            cls._fast = get_fast_provider()

        return cls._fast
