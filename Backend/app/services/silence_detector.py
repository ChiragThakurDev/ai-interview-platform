import time


class SilenceDetector:
    """
    Detects when candidate stops speaking.

    Used for:
    - finishing answer
    - triggering AI evaluation
    """


    def __init__(
        self,
        silence_seconds: float = 3.0,
    ):

        self.silence_seconds = silence_seconds

        self.last_audio_time = time.time()



    def update(self):

        self.last_audio_time = time.time()



    def is_silent(self) -> bool:

        elapsed = (
            time.time()
            -
            self.last_audio_time
        )


        return (
            elapsed
            >= self.silence_seconds
        )



    def reset(self):

        self.last_audio_time = time.time()
