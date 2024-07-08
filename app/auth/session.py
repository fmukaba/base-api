import pickle
from uuid import uuid4
from fastapi import Request, Response
from redis.asyncio import Redis
from core.config import settings
from auth.schemas import SessionData

class SessionStorage:
    def __init__(self):
        self.client = Redis.from_url(url=(settings.redis_url))

    async def get_item(self, key: str):
        raw = await self.client.get(key)
        return pickle.loads(raw)
        # return raw

    async def set_item(self, key: str, value: SessionData):
        await self.client.set(key, pickle.dumps(value, protocol=pickle.HIGHEST_PROTOCOL), ex=settings.expire_time)
        # await self.client.set(key, value)

    async def delete_item(self, key: str):
        await self.client.delete(key)

    async def generate_session_id(self) -> str:
        session_id = uuid4().hex
        while await self.client.get(session_id):
            session_id = uuid4().hex
        return session_id
    
class SessionManager:
    def __init__(self):
        self.storage = SessionStorage()

    async def set_session(self, response: Response, data: SessionData):
        session_id = await self.storage.generate_session_id()
        await self.storage.set_item(session_id, data)
        response.set_cookie(settings.session_cookie_name, session_id, httponly=True, secure=True, samesite="Lax", max_age=settings.max_age)
        return session_id

    async def get_session(self, request: Request):
        session_id = request.cookies.get(settings.session_cookie_name, "")
        session_data = await self.storage.get_item(session_id)
        if session_data:
            return session_data 
        return None

    async def delete_session(self, request: Request, response: Response):
        session_id = request.cookies.get(settings.session_cookie_name, "")
        response.delete_cookie(settings.session_cookie_name)
        await self.storage.delete_item(session_id)

session_manager = SessionManager()