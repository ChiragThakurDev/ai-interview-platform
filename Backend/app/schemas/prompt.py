from datetime import datetime

from pydantic import BaseModel, Field


# ==========================================
# Create Prompt
# ==========================================

class PromptCreate(BaseModel):

    name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    version: str = Field(
        ...,
        min_length=1,
        max_length=50
    )

    template: str

    provider: str = "ollama"

    model: str = "llama3.1:8b"

    temperature: float = Field(
        default=0.3,
        ge=0.0,
        le=2.0
    )

    is_active: bool = False



# ==========================================
# Update Prompt
# ==========================================

class PromptUpdate(BaseModel):

    template: str | None = None

    provider: str | None = None

    model: str | None = None

    temperature: float | None = Field(
        default=None,
        ge=0.0,
        le=2.0
    )

    is_active: bool | None = None



# ==========================================
# Response
# ==========================================

class PromptResponse(BaseModel):

    id: int

    name: str

    version: str

    template: str

    provider: str | None

    model: str | None

    temperature: float | None

    is_active: bool

    created_at: datetime


    class Config:
        from_attributes = True
