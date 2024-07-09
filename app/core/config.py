import os
from dotenv import load_dotenv
from datetime import timedelta
from uuid import uuid4

load_dotenv()

class Settings():
    env_name=os.getenv('ENV', 'LOCAL')
    config_file='app_config.json'
    secret_key: str = os.getenv("SECRET_KEY", uuid4().hex)
    fernet_key: str = os.getenv("FERNET_KEY", uuid4().hex)
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    redis_url: str = os.getenv("REDIS_URL")
    session_cookie_name="session"
    session_expire_time: timedelta = timedelta(hours=6)
    cookie_max_age: int = 3600 * 24
settings = Settings()

