from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CodingDraftResponse(BaseModel):

    id: int

    user_id: int

    question_id: int

    language: str

    code: str

    updated_at: datetime


    model_config = ConfigDict(
        from_attributes=True
    )
