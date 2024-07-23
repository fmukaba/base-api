from pydantic import BaseModel, Json


class Message(BaseModel):
    id: int
    group_id: int
    sender_id: int
    body: Json