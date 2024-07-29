from typing import Optional
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, Response, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi_login.exceptions import InvalidCredentialsException
from pydantic import EmailStr
from sqlalchemy.orm import Session
from core.database import get_db
from core.config import settings
from users.crud import  pwd_context, get_user_by_username, get_user_by_email, get_user_by_id, update_user 
from users.models import User 
from auth.schemas import Login, SessionData
from auth.session import get_session, set_session, delete_session
from auth.utils import *
from notifications.schemas import EmailSchema
from notifications.utils import send_reset_password_email, env, templates_dir

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
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="User is not verified")
    # create a new session
    session_data = create_session_data_from_user(user)
    response = Response(status_code=200)
    try:
        await set_session(response, session_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Login Failed. Check the logs for more information.")
    return response

@router.get("/verify-email/{token}")
async def verify_email(token: str, db: Session = Depends(get_db)):
    user_id: int = verify_email_token(token)
    user: User = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        update_user(db, user, {"is_verified": True})
    except Exception as e:
        raise HTTPException(status_code=500, detail="Something went wrong. Check the logs for more details")
    
    return {"message": "Email verified successfully"}

@router.post("/logout")
@login_required()
async def logout(request: Request, session: Optional[SessionData] = Depends(get_session)):
    response = Response(status_code=200)
    try:
        await delete_session(request, response)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Logout Failed. Check the logs for more information.")
    return response

@router.post("/reset-password")
async def reset_password(email: EmailStr, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    user: User = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    token = generate_verification_token(user.id)
    verification_url = f"{settings.api_host}/auth/reset-password/{token}"
    email = EmailSchema(target=user.email, subject="Password reset request")

    background_tasks.add_task(send_reset_password_email, email, verification_url)

    return {"message": "Reset email is being sent"}

@router.get("/reset-password/{token}")
async def reset_password(token: str, db: Session = Depends(get_db)):
    user_id: int = verify_email_token(token)
    user: User = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Request not allowed")
    
    template = env.get_template('reset_password_form.html')
    response = HTMLResponse(template.render(token=token))

    return response

@router.post("/update-password")
async def update_password(token: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user_id: int = verify_email_token(token)
    user: User = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Request not allowed")
    
    hashed_password: str = pwd_context.hash(password)
    update_fields = {"hashed_password": hashed_password}

    update_user(db, user, update_fields)

    return RedirectResponse(url=f'{settings.frontend_host}?status=success', status_code=303)

@router.get("/session")
@login_required()
async def get_session(session: Optional[SessionData] = Depends(get_session)): 
    response = Response(status_code=200)
    print(session)
    return response

@router.get("/admin")
@admin_restricted()
async def get_sesh_test(session: Optional[SessionData] = Depends(get_session)): 
    print(session)
    response = Response(status_code=200)
    return response