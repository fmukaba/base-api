from typing import Optional
from fastapi import APIRouter, Depends, Request, Response
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from db.database import get_db
from users.crud import get_user_by_username, pwd_context
from auth.schemas import Login, SessionData
from auth.session import session_manager
from auth.utils import create_session_data_from_user, login_required

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
    session_data = create_session_data_from_user(user)
    response = JSONResponse(content='success')
    await session_manager.set_session(response, session_data)
    return response

@router.post("/logout")
@login_required()
async def logout(request: Request, response: Response, session: Optional[SessionData] = Depends(session_manager.get_session)):
    response = JSONResponse(content="Successfully logged out")
    await session_manager.delete_session(request, response)
    return response

@router.get("/getsesh")
@login_required()
async def get_sesh_test(request: Request): 
    session_data = await session_manager.get_session(request)
    return session_data

