from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from functools import wraps
from core.config import settings
from users.models import User
from auth.schemas import SessionData
from auth.session import session_manager

# User loader function
def load_user(request: Request):
    user_data = session_manager.get_session(request)
    if user_data is None:
        return None
    return user_data

# Decorator to check authentication
def login_required():
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            session_id = request.cookies.get(settings.session_cookie_name)
            if not session_id:
                raise HTTPException(status_code=401, detail="Not authenticated")

            user = load_user(request)
            if not user:
                raise HTTPException(status_code=401, detail="Not authenticated")
            # request.state.user = user
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator

def create_session_data_from_user(user: User) -> SessionData:
    session_data = SessionData (
        user_id=user.id,
        username=user.username,
        email=user.email
    )
    return session_data