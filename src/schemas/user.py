from typing import Optional

from pydantic import BaseModel


class UserSchema(BaseModel):
    user_id: str
    first_name: str
    last_name: Optional[str]
    username: Optional[str]
