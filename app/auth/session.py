import pickle
from typing import Optional
from uuid import uuid4
from fastapi import Depends, Request, Response
from redis.asyncio import Redis
from core.config import settings
from auth.schemas import SessionData

class SessionStorage:
    def __init__(self):
        self.client = Redis.from_url(url=(settings.redis_url))

    async def get_item(self, key: str) -> Optional[SessionData]:
        raw = await self.client.get(key)
        if raw:
            return pickle.loads(raw)
        return None

    async def set_item(self, key: str, value: SessionData):
        await self.client.set(key, pickle.dumps(value, protocol=pickle.HIGHEST_PROTOCOL), ex=settings.expire_time)

    async def delete_item(self, key: str):
        await self.client.delete(key)

    async def generate_session_id(self) -> str:
        session_id = uuid4().hex
        while await self.client.get(session_id):
            session_id = uuid4().hex
        return session_id
    
    async def print_all(self):
        async for key in self.client.scan_iter():
            print("[ ", key, " => " , await self.client.get(key) , " ]\n")
    
    async def close(self):
        await self.client.close()
    
async def set_session(response: Response, data: SessionData) -> str:
    storage =  SessionStorage()
    session_id = await storage.generate_session_id()
    await storage.set_item(session_id, data)
    response.set_cookie(settings.session_cookie_name, session_id, httponly=True, secure=True, samesite="Lax", max_age=settings.max_age)
    await storage.close()
    return session_id

async def get_session(request: Request) -> Optional[SessionData]:
    storage =  SessionStorage()
    session_id = request.cookies.get(settings.session_cookie_name, "")
    session_data = await storage.get_item(session_id)
    await storage.close()
    return session_data

async def delete_session(request: Request, response: Response):
    storage =  SessionStorage()
    session_id = request.cookies.get(settings.session_cookie_name, "")
    response.delete_cookie(settings.session_cookie_name)
    await storage.delete_item(session_id)
    await storage.close()