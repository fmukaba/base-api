from fastapi import HTTPException
from cryptography.fernet import Fernet
from functools import wraps
from users.models import User
from auth.schemas import SessionData

def login_required():
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = kwargs.get('request')
            session = kwargs.get('session')
            if not session:
                delete_session_cookie={'Set-Cookie': 'session=; Max-Age=0; Path=/; HttpOnly'}
                raise HTTPException(status_code=401, 
                                    detail="Not authenticated", 
                                    headers=delete_session_cookie)
            return await func(*args, **kwargs)
        return wrapper
    return decorator

def create_session_data_from_user(user: User) -> SessionData:
    session_data = SessionData(
        user_id=user.id,
        username=user.username,
        email=user.email
    )
    return session_data