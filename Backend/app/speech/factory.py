from app.core.config import settings

from app.speech.providers.base import BaseSpeechProvider
from app.speech.providers.faster_whisper_provider import (
    FasterWhisperProvider,
)


class SpeechFactory:

    @staticmethod
    def get_provider() -> BaseSpeechProvider:

        if settings.speech_provider == "faster-whisper":
            return FasterWhisperProvider()

        raise ValueError(
            f"Unsupported speech provider: "
            f"{settings.speech_provider}"
        )
