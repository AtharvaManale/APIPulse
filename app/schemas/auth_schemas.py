from pydantic import BaseModel

class RegistrationSchema(BaseModel):
    username: str
    password: str
    email_id: str

class LoginSchema(BaseModel):
    username: str
    password: str