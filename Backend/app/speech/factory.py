from app.core.config import settings
from app.speech.base import SpeechProvider
from app.speech.faster_whisper_provider import (
    FasterWhisperProvider,
)


class SpeechFactory:

    @staticmethod
    def get_provider() -> SpeechProvider:

        if settings.speech_provider == "faster-whisper":
            return FasterWhisperProvider()

        raise ValueError(
            f"Unsupported speech provider: "
            f"{settings.speech_provider}"
        )
