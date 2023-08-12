from pydantic import BaseModel


class AdminSchema(BaseModel):
    username: str
    hashed_password: str


class LoginAdminSchema(BaseModel):
    login: str
    password: str
