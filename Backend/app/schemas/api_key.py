from datetime import datetime
from pydantic import BaseModel, Field


# -------------------------
# Request Schema
# -------------------------
class APIKeyCreate(BaseModel):
    name: str
    permissions: str = Field(
        default="read",
        description="Comma-separated permissions (e.g. read,write)",
    )


# -------------------------
# Response Schema
# -------------------------
class APIKeyResponse(BaseModel):
    id: int
    name: str
    api_key: str
    permissions: str
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
    permissions: str
    is_active: bool
    expires_at: datetime | None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
