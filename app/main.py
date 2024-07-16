
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from auth.router import router as auth_router
from users.router import router as users_router
from notifications.router import router as notifications_router
from core.config import settings

logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(notifications_router)