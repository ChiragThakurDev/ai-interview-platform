from abc import ABC, abstractmethod


class SpeechProvider(ABC):
    """
    Base interface for all Speech-to-Text providers.
    """

    @abstractmethod
    def transcribe(
        self,
        audio_path: str,
    ) -> dict:
        """
        Transcribe an audio file.

        Returns:
            {
                "language": str,
                "transcript": str,
                "segments": list
            }
        """
        raise NotImplementedError
