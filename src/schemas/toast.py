from pydantic import BaseModel


class Toast(BaseModel):
    message: str
    error: bool
