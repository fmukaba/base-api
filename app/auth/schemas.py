from pydantic import BaseModel

class Login(BaseModel):
    username: str
    password: str

class JWTToken(BaseModel):
    access_token: str
    token_type: str

class SessionData(BaseModel):
    user_id: int
    username: str
    email: str

    def to_dict(self):
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
    
class JSONClientMetadata(BaseModel):
    pass
