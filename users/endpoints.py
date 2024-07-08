from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .crud import get_user_by_email, create_user
from .schemas import User, UserCreate
from db.database import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)
