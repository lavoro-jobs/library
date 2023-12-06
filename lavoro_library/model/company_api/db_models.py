import uuid

from enum import Enum

from typing import Union

from pydantic import BaseModel


class RecruiterRole(str, Enum):
    admin = "admin"
    employee = "employee"


class Company(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    logo: Union[bytes, None] = None


class RecruiterProfile(BaseModel):
    account_id: uuid.UUID
    company_id: uuid.UUID
    first_name: str
    last_name: str
    company_id: uuid.UUID
    recruiter_role: RecruiterRole


class InviteToken(BaseModel):
    token: str
    email: str
    company_id: uuid.UUID
