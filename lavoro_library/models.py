import inspect
import uuid

from datetime import datetime
from enum import Enum
from typing import Annotated, Union

from fastapi import Form
from pydantic import BaseModel, EmailStr


def as_form(cls):
    new_params = [
        inspect.Parameter(
            field_name,
            inspect.Parameter.POSITIONAL_ONLY,
            default=model_field.default,
            annotation=Annotated[model_field.annotation, model_field.metadata, Form()],
        )
        for field_name, model_field in cls.model_fields.items()
    ]

    cls.__signature__ = cls.__signature__.replace(parameters=new_params)

    return cls


class Role(str, Enum):
    applicant = "applicant"
    employer = "employer"


@as_form
class RegistrationForm(BaseModel):
    email: Annotated[EmailStr, Form()]
    password: Annotated[str, Form()]
    role: Annotated[Role, Form()]
    

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


class PositionCatalog(BaseModel):
    id: int
    position_name: str


class EducationCatalog(BaseModel):
    id: int
    education_level: str


class ContractTypeCatalog(BaseModel):
    id: int
    contract_type: str


class WorkTypeCatalog(BaseModel):
    id: int
    work_type: str


class SkillsCatalog(BaseModel):
    id: int
    skill_name: str
