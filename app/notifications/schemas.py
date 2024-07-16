from pydantic import BaseModel, EmailStr

class EmailSchema(BaseModel):
    target: EmailStr
    subject: str = "Subject"
    body: str = ""