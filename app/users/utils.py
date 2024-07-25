from typing import Optional
from fastapi import HTTPException
import jwt
from datetime import datetime, timezone, timedelta
from core.config import settings

def generate_verification_token(user_id: int) -> str:
    payload = {
        'user_id': user_id,
        'exp': datetime.now(timezone.utc) + timedelta(seconds=settings.jwt_expiry_time)
    }
    return jwt.encode(payload, settings.jwt_secret, settings.jwt_algorithm)

def verify_email_token(token: str) -> Optional[int]:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")