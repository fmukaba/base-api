from datetime import datetime

from pydantic import BaseModel, Unity, Json


#todo: change sender to user object. user object should have avatar url
#todo: isSeen: bool
class Message(BaseModel):
    sender: str
    message: Unity[str, Json]
    timestamp: datetime
