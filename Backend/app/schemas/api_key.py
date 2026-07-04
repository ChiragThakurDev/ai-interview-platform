from datetime import datetime
from pydantic import BaseModel


# -------------------------
# Request Schema
# -------------------------
class APIKeyCreate(BaseModel):
    name: str


# -------------------------
# Response Schema
# -------------------------
class APIKeyResponse(BaseModel):
    id: int
    name: str
    api_key: str
    is_active: bool
    expires_at: datetime | None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


# -------------------------
# List Response Schema
# -------------------------
class APIKeyListResponse(BaseModel):
    id: int
    name: str
    is_active: bool
    expires_at: datetime | None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
