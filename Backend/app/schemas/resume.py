from datetime import datetime
from pydantic import BaseModel


class ResumeResponse(BaseModel):
    id: int
    filename: str
    file_path: str
    file_size: int
    content_type: str
    uploaded_at: datetime
    user_id: int

    class Config:
        from_attributes = True
