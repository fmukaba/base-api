from core.database import Base, engine
from sqlalchemy import Column, DateTime, Integer, func, JSON


class Message(Base):
    __tablename__ = "Messages"
    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, index=True)
    sender_id = Column(Integer, index=True)
    body = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# Create the database tables
Base.metadata.create_all(bind=engine)
