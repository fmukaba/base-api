import os
from datetime import timedelta
from uuid import uuid4

from dotenv import load_dotenv

load_dotenv()


class Settings:
    env_name = os.getenv('ENV', 'LOCAL')
    config_file = 'app_config.json'
    api_host: str = "http://127.0.0.1:8000"
    secret_key: str = os.getenv("SECRET_KEY", uuid4().hex)
    fernet_key: str = os.getenv("FERNET_KEY", uuid4().hex)

    # session
    session_cookie_name = "session"
    session_expiry_time: timedelta = timedelta(hours=6)
    cookie_max_age: int = 24 * 3600

    # jwt
    jwt_secret: str = os.getenv("JWT_SECRET")
    jwt_algorithm: str = "HS256"
    jwt_expiry_time: int = 3600

    # base database
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")

    # postgres
    postgres_db: str = os.getenv("POSTGRES_DB")
    postgres_user: str = os.getenv("POSTGRES_USER")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD")

    # redis
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379")

    # email config
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: str = os.getenv("SMTP_USERNAME")
    smtp_password: str = os.getenv("SMTP_PASSWORD")


settings = Settings()
