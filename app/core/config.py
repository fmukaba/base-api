from datetime import timedelta
import os
from uuid import uuid4

class Settings():
    env_name=os.getenv('ENV', 'LOCAL')
    config_file='app_config.json'
    secret_key: str = os.getenv("SECRET_KEY", uuid4().hex)
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    expire_time: timedelta = timedelta(hours=6)
    max_age: int = 3600 * 24
    session_cookie_name="session"
settings = Settings()

