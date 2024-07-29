from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from core.config import settings
from auth.utils import generate_verification_token
from notifications.schemas import EmailSchema
from notifications.utils import send_verification_email
from users.crud import get_user_by_email, create_user
from users.schemas import User, UserCreate

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=User)
def create_user_route(user: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = create_user(db=db, user=user)
    token = generate_verification_token(new_user.id)
    verification_url = f"{settings.api_host}/auth/verify-email/{token}"
    email = EmailSchema(target=new_user.email, subject="Please verify your email")

    background_tasks.add_task(send_verification_email, email, verification_url)
 
    return new_user