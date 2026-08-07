from faster_whisper import WhisperModel

from app.core.config import settings
from app.speech.providers.base import BaseSpeechProvider


class FasterWhisperProvider(BaseSpeechProvider):

    _model = None

    def __init__(self):

        if FasterWhisperProvider._model is None:
            FasterWhisperProvider._model = WhisperModel(
                settings.whisper_model,
                device="cpu",
                compute_type="int8",
            )

        self.model = FasterWhisperProvider._model

    def transcribe(
        self,
        audio_path: str,
    ) -> str:

        segments, _ = self.model.transcribe(audio_path)

        return " ".join(
            segment.text.strip()
            for segment in segments
        ).strip()

    def stream_transcribe(
        self,
        audio_chunk: bytes,
    ) -> str:
        """
        Placeholder for live streaming transcription.
        This will be implemented when we integrate
        the WebSocket audio pipeline.
        """
        raise NotImplementedError(
            "Streaming transcription is not implemented yet."
        )
