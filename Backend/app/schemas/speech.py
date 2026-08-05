from pydantic import BaseModel


class SpeechSegment(BaseModel):

    start: float

    end: float

    text: str


class SpeechResponse(BaseModel):

    success: bool

    language: str

    transcript: str

    segments: list[SpeechSegment]
