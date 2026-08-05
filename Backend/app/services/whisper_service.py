import os
import shutil
import tempfile

from fastapi import UploadFile

from app.speech.factory import SpeechFactory


class WhisperService:

    def __init__(self):

        self.provider = SpeechFactory.get_provider()

    def transcribe(
        self,
        file: UploadFile,
    ) -> dict:

        suffix = os.path.splitext(
            file.filename
        )[1]

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as temp_file:

            shutil.copyfileobj(
                file.file,
                temp_file,
            )

            temp_path = temp_file.name

        try:

            result = self.provider.transcribe(
                temp_path,
            )

            return result

        finally:

            if os.path.exists(
                temp_path,
            ):
                os.remove(
                    temp_path,
                )
