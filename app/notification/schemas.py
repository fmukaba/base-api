from pydantic import BaseModel, Union, Dict, Any, Json


class Notification(BaseModel):
    topic_arn: str
    target_arn: str
    phone_number: str
    message: Union[str, Json[Any]]
    subject: str
    message_structure: str
    message_attributes: Dict[str, Dict[str, Any]]
    message_deduplication_id: str
    message_group_id: str


class Topic(BaseModel):
    arn: str
    protocol: str
    endpoint: str
