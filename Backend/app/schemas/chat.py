from datetime import datetime

from pydantic import BaseModel



# =====================================================
# Chat Session
# =====================================================


class ChatSessionCreate(BaseModel):

    title: str = "New Chat"



class ChatSessionResponse(BaseModel):

    id: int
    title: str
    created_at: datetime


    model_config = {
        "from_attributes": True
    }



# =====================================================
# Chat Message
# =====================================================


class ChatMessageCreate(BaseModel):

    message: str



class ChatMessageResponse(BaseModel):

    id: int
    role: str
    content: str
    created_at: datetime


    model_config = {
        "from_attributes": True
    }
