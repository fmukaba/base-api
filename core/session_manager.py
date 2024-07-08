import uuid
from redis.asyncio import Redis

class SessionManager:
    def __init__(self, redis: Redis):
        self.redis = redis

    def generate_session_id(self):
        return uuid.uuid4().hex

    async def set_session(self, session_id: str, data: dict):
        await self.redis.set(session_id, str(data))

    async def get_session(self, session_id: str):
        session_data = await self.redis.get(session_id)
        if session_data:
            return session_data 
        return None

    async def delete_session(self, session_id: str):
        await self.redis.delete(session_id)