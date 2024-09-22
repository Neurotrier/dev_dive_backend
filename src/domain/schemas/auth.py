from pydantic import BaseModel


class AuthSignup(BaseModel):
    username: str
    email: str
    password: str
