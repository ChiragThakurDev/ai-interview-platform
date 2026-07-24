from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ResumeResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int

    filename: str

    file_path: str

    file_size: int

    content_type: str

    uploaded_at: datetime

    user_id: int
