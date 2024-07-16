from typing import Optional
from fastapi import APIRouter, BackgroundTasks, Depends
from notifications.schemas import EmailSchema
from notifications.utils import send_email

router = APIRouter(
    prefix="/notify",
    tags=["notify"],
    responses={404: {"description": "Not found"}},
)

@router.post("/send-email")
async def send_email_endpoint(email: EmailSchema, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email, email)
    return {"message": "Email is being sent in the background"}