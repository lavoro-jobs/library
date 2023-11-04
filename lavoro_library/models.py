import uuid

from datetime import datetime
from enum import Enum
from typing import Annotated, Union

from fastapi import Form
from pydantic import BaseModel, EmailStr, SecretStr



class Role(str, Enum):
    applicant = "applicant"
    employer = "employer"


class RegistrationForm(BaseModel):
    email: Annotated[EmailStr, Form()]
    password: Annotated[SecretStr, Form()]
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
