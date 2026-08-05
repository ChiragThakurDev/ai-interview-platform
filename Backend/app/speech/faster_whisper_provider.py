from faster_whisper import WhisperModel

from app.core.config import settings
from app.speech.base import SpeechProvider


class FasterWhisperProvider(SpeechProvider):
    """
    Faster-Whisper implementation with automatic
    GPU -> CPU fallback.
    """

    def __init__(self):

        try:

            self.model = WhisperModel(
                settings.whisper_model,
                device=settings.whisper_device,
                compute_type=settings.whisper_compute_type,
            )

            print(
                f"[Whisper] Using {settings.whisper_device.upper()} backend"
            )

        except Exception as e:

            print(
                f"[Whisper] Failed to initialize "
                f"{settings.whisper_device}: {e}"
            )

            print(
                "[Whisper] Falling back to CPU..."
            )

            self.model = WhisperModel(
                settings.whisper_model,
                device="cpu",
                compute_type="int8",
            )

    def transcribe(
        self,
        audio_path: str,
    ) -> dict:

        segments, info = self.model.transcribe(
            audio_path,
        )

        transcript = []

        segment_list = []

        for segment in segments:

            text = segment.text.strip()

            transcript.append(text)

            segment_list.append(
                {
                    "start": segment.start,
                    "end": segment.end,
                    "text": text,
                }
            )

        return {
            "language": info.language,
            "transcript": " ".join(transcript),
            "segments": segment_list,
        }
