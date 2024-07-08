from fastapi import APIRouter, Depends, Request, Response
from fastapi_login.exceptions import InvalidCredentialsException
from sqlalchemy.orm import Session
from users.crud import get_user_by_username, pwd_context
from db.database import get_db
from auth.schemas import Login
from fastapi.responses import JSONResponse
from redis.asyncio import from_url
from core.session_manager import SessionManager
from core.config import settings

redis = from_url(settings.redis_url, decode_responses=True)
session_manager = SessionManager(redis)

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

@router.post("/login")
async def login(request: Request, response: Response, data: Login, db: Session = Depends(get_db)):
    username = data.username
    password = data.password
    user = get_user_by_username(db, username)

    if not user or not pwd_context.verify(password, user.hashed_password):
        raise InvalidCredentialsException
    
    # create a new session
    session_id = session_manager.generate_session_id()
    await session_manager.set_session(session_id, user.id)
    response = JSONResponse(content="success")
    response.set_cookie(key="session", value=session_id, httponly=True, secure=True, samesite="Lax", max_age=24*3600)

    return response

@router.post("/logout")
async def logout(request: Request):
    session_id = request.cookies.get("session")
    print(session_id)
    if session_id:
        await session_manager.delete_session(session_id)
        response = JSONResponse(content="Successfully logged out")
        response.delete_cookie("session")
        return response
    return JSONResponse(content="No session found")

@router.get("/getsesh")
async def getseshtest(request: Request): 
    session_data = await session_manager.get_session(request.cookies.get("session") or 'none')
    return session_data

