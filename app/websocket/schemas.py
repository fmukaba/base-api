from datetime import datetime

from pydantic import BaseModel


class Message(BaseModel):
    id: int
    group_id: int
    sender_id: int
    message: str
    created_at: datetime
    updated_at: datetime
