from pydantic import BaseModel

class Login(BaseModel):
    username: str
    password: str

class JWTToken(BaseModel):
    access_token: str
    token_type: str
