from functools import wraps
from typing import Optional
from fastapi import HTTPException, Request
from core.config import settings
from users.models import User
from auth.schemas import SessionData

def login_required():
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get('request')
            session: Optional[SessionData] = kwargs.get('session')
            cookie = request.cookies.get(settings.session_cookie_name,"")
            delete_session_cookie={'Set-Cookie': f'{settings.session_cookie_name}=; Max-Age=0; Path=/; HttpOnly'}
            if not session:
                if cookie:
                    raise HTTPException(status_code=401, 
                                        detail="Session timed out", 
                                    headers=delete_session_cookie)
                else:
                    raise HTTPException(status_code=401, 
                                        detail="User is not authenticated", 
                                    headers=delete_session_cookie)
            return await func(*args, **kwargs)
        return wrapper
    return decorator

def admin_restricted():
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            await login_required()(func)(*args, **kwargs)
            session: SessionData = kwargs.get('session')
            if not session.is_admin:
                raise HTTPException(status_code=403, detail="User is not an admin")
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def create_session_data_from_user(user: User) -> SessionData:
    session_data = SessionData(
        user_id=user.id,
        username=user.username,
        email=user.email,
        is_admin=user.is_admin
    )
    return session_data