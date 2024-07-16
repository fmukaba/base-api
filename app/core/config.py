import os
from dotenv import load_dotenv
from datetime import timedelta
from uuid import uuid4

load_dotenv()


class Settings():
    env_name=os.getenv('ENV', 'LOCAL')
    config_file='app_config.json'
    api_host: str = "http://127.0.0.1:8000"
    secret_key: str = os.getenv("SECRET_KEY", uuid4().hex)
    fernet_key: str = os.getenv("FERNET_KEY", uuid4().hex)
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    session_cookie_name="session"
    session_expiry_time: timedelta = timedelta(hours=6)
    cookie_max_age: int = 24 * 3600 
    # email config
    smtp_server : str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: str = os.getenv("SMTP_USERNAME")
    smtp_password: str = os.getenv("SMTP_PASSWORD") 
    # jwt
    jwt_secret: str = os.getenv("JWT_SECRET")
    jwt_algorithm: str = "HS256"
    jwt_expiry_time: int = 3600
    # postgres
    postgres_user: str = os.getenv("POSTGRES_USER", "admin")
    postgres_pw: str = os.getenv("POSTGRES_PASSWORD", uuid4().hex)
    # pgadmin4
    pgadmin_email: str = os.getenv("PGADMIN_EMAIL", "admin@admin.com")
    pgadmin_password: str = os.getenv("PGADMIN_PASSWORD", "root")
    
settings = Settings()

