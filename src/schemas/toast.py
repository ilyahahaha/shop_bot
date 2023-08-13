from pydantic import BaseModel


class ToastSchema(BaseModel):
    message: str
