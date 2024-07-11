from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, create_engine, func, JSON
from users.models import User
from db.database import Base, engine

class Sessions(Base):
    __tablename__ = "sessions"
    user_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"), primary_key=True)
    session_id = Column(String, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now())
    expires_at = Column(DateTime)
    device_metadata = Column(JSON)

# Create the database tables
Base.metadata.create_all(bind=engine)
