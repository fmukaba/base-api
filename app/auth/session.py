import json
from typing import Optional
from uuid import uuid4
from fastapi import Request, Response
from cryptography.fernet import Fernet
from redis.asyncio import Redis
from core.config import settings
from auth.schemas import SessionData

class SessionStorage:
    def __init__(self):
        self.client = Redis.from_url(url=(settings.redis_url))
        self.fernet = Fernet(settings.fernet_key)

    async def get_item(self, key: str) :
        return await self.client.get(key)

    async def set_item(self, key: str, value: SessionData):
        await self.client.set(key, value, ex=settings.session_expiry_time)

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
    # encrypt session data with fernet
    session_data_dict = data.to_dict()
    session_data_json = json.dumps(session_data_dict)
    encrypted_session_data = storage.fernet.encrypt(session_data_json.encode())
    # set encrypted data in storage
    await storage.set_item(session_id, encrypted_session_data)
    # set session in the response cookie
    response.set_cookie(settings.session_cookie_name, 
                        session_id, 
                        httponly=True, 
                        secure=True, 
                        samesite="Lax", 
                        max_age=settings.cookie_max_age)
    await storage.close()
    return session_id

async def get_session(request: Request) -> Optional[SessionData]:
    storage =  SessionStorage()
    session_id = request.cookies.get(settings.session_cookie_name, "")
    # extend the session life on every interaction
    if await storage.client.exists(session_id):
        await storage.client.expire(session_id, settings.session_expiry_time)
    session_data = await storage.get_item(session_id)
    # decrypt stored session data
    if session_data:
        try:
            session_data_json = storage.fernet.decrypt(session_data).decode()
            session_data_dict = json.loads(session_data_json)
            session_data = SessionData.from_dict(session_data_dict)
        except Exception as e:
            print(e)
            return None
    await storage.close()
    return session_data

async def delete_session(request: Request, response: Response):
    storage =  SessionStorage()
    session_id = request.cookies.get(settings.session_cookie_name, "")
    # removie session cookie from response
    response.delete_cookie(settings.session_cookie_name)
    await storage.delete_item(session_id)
    await storage.close()