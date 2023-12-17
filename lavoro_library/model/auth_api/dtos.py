from typing import Annotated, Union

from fastapi import Form
from pydantic import BaseModel, EmailStr

from lavoro_library.model.auth_api.db_models import Role
from lavoro_library.model.shared import as_form


@as_form
class RegisterDTO(BaseModel):
    email: Annotated[EmailStr, Form()]
    password: Annotated[str, Form()]
    role: Annotated[Role, Form()]


@as_form
class LoginDTO(BaseModel):
    grant_type: Annotated[Union[str, None], Form(pattern="password")] = None
    username: Annotated[str, Form()]
    password: Annotated[str, Form()]
    scope: Annotated[str, Form()] = ""
    client_id: Annotated[Union[str, None], Form()] = None
    client_secret: Annotated[Union[str, None], Form()] = None


class AccountDTO(BaseModel):
    email: str
    is_active: bool
    role: str


class TokenDTO(BaseModel):
    access_token: str
    token_type: str


class TokenDataDTO(BaseModel):
    email: Union[str, None] = None
