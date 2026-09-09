from pydantic import BaseModel
import email

class RegistrationSchema(BaseModel):
    username: str
    password: str
    email_id: email

class LoginSchema(BaseModel):
    username: str
    password: str