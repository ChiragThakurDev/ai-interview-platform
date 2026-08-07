from app.speech.factory import SpeechFactory


class SpeechService:

    def __init__(self):

        self.provider = SpeechFactory.get_provider()

    def transcribe(
        self,
        audio_path: str,
    ):

        return self.provider.transcribe(
            audio_path
        )

    def stream_transcribe(
        self,
        chunk: bytes,
    ):

        return self.provider.stream_transcribe(
            chunk
        )
