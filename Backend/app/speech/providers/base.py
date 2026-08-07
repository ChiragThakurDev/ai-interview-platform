from abc import ABC, abstractmethod


class BaseSpeechProvider(ABC):

    @abstractmethod
    def transcribe(
        self,
        audio_path: str,
    ) -> str:
        """
        Convert an audio file into text.
        """
        raise NotImplementedError

    @abstractmethod
    def stream_transcribe(
        self,
        audio_chunk: bytes,
    ) -> str:
        """
        Stream partial transcription.
        """
        raise NotImplementedError
