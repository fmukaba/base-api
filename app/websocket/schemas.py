from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Unity, Json


class Message(BaseModel):
    id: uuid4
    group_id: uuid4
    sender_id: str
    message: Unity[str, Json]
    created_at: datetime
    updated_at: datetime
