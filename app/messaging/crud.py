from sqlalchemy.orm import Session

from models import Message


def create_message(db: Session, message: Message) -> Message:
    db_message = Message(
        group_id=message.group_id,
        sender_id=message.sender_id,
        body=message.body
    )
    db.add(db_message)
    db.commit()
    return db_message


def delete_message(db: Session, message_id: int):
    db.query(Message).delete(Message.id == message_id)


def list_messages_by_group_id(db: Session, group_id: int):
    db_messages = db.query(Message).filter(Message.group_id == group_id).all()
    return db_messages
