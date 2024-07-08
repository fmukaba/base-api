from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from functools import wraps
from core.constants import SESSION_COOKIE_NAME
from core import session_manager


# User loader function
async def load_user(session_id: str):
    user_data = await session_manager.get_session(session_id)
    if user_data is None:
        return None
    return user_data

# Decorator to check authentication
def login_required():
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            session_id = request.cookies.get(SESSION_COOKIE_NAME)
            if not session_id:
                raise HTTPException(status_code=401, detail="Not authenticated")

            user = await load_user(session_id)
            if not user:
                raise HTTPException(status_code=401, detail="Not authenticated")

            request.state.user = user
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator