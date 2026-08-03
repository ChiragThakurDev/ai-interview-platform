from datetime import datetime

from pydantic import BaseModel


class PromptExecutionResponse(BaseModel):
    id: int
    prompt_name: str
    prompt_version: str
    provider: str | None
    model: str | None
    variables: str | None
    rendered_prompt: str
    response: str | None
    success: bool
    latency: float | None
    created_at: datetime

    class Config:
        from_attributes = True
