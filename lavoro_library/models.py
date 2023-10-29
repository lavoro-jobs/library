import datetime
import uuid

from typing import Annotated, Union
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None


class User(BaseModel):
    email: str
    is_active: bool
    role: str


class UserInDB(User):
    id: uuid.UUID
    password_hash: str
    created_on: datetime