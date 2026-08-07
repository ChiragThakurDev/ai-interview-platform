from pydantic import BaseModel


class TranscriptResult(BaseModel):

    text: str

    language: str | None = None

    confidence: float | None = None

    is_final: bool = True
