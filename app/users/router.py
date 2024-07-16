from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session
from notifications.schemas import EmailSchema
from notifications.utils import send_verification_email
from users.crud import get_user_by_email, create_user, get_user_by_id, update_user
from users.schemas import User, UserCreate
from users.models import User as UserModel
from users.utils import generate_verification_token, verify_token
from core.database import get_db
from core.config import settings

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
    verification_url = f"{settings.api_host}/users/verify-email/{token}"
    email = EmailSchema(target="fxkikomina@gmail.com", subject="Please verify your email")

    background_tasks.add_task(send_verification_email, email, verification_url)
 
    return new_user

@router.get("/verify-email/{token}")
async def verify_email(token: str, db: Session = Depends(get_db)):
    user_id: int = verify_token(token)
    user: UserModel = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        update_user(db, user, {"is_verified": True})
    except Exception as e:
        raise HTTPException(status_code=500, detail="Something went wrong. Check the logs for more details")
    
    return {"message": "Email verified successfully"}