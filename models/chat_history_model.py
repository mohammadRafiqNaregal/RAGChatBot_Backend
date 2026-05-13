from datetime import datetime

from pydantic import BaseModel


class ChatHistoryResponse(BaseModel):
    id: int
    user_id: int
    question: str
    response: str
    timestamp: datetime

    class Config:
        from_attributes = True


class ChatHistoryListResponse(BaseModel):
    count: int
    items: list[ChatHistoryResponse]