from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request, Response, logger
from fastapi_login.exceptions import InvalidCredentialsException
from sqlalchemy.orm import Session
from db.database import get_db
from users.crud import get_user_by_username, pwd_context
from auth.schemas import Login, SessionData
from auth.session import get_session, set_session, delete_session
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
    response = Response(status_code=200)
    await set_session(response, session_data)
    return response

@router.post("/logout")
@login_required()
async def logout(request: Request, session: Optional[SessionData] = Depends(get_session)):
    response = Response(status_code=200)
    try:
        await delete_session(request, response)
    except Exception as e:
        logger.logger.error(e)
        raise HTTPException(status_code=500, detail="Logout Failed. Check the logs for more information.")
    return response

@router.get("/getsesh")
@login_required()
async def get_sesh_test(request: Request, session: Optional[SessionData] = Depends(get_session)): 
    response = Response(status_code=200)
    print(session)
    return response