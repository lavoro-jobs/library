import uuid

from enum import Enum

from typing import Union

from sqlmodel import SQLModel


class RecruiterRole(str, Enum):
    admin = "admin"
    employee = "employee"


class Company(SQLModel):
    id: uuid.UUID
    name: str
    description: str
    logo: Union[bytes, None] = None


class RecruiterProfile(SQLModel):
    account_id: uuid.UUID
    company_id: uuid.UUID
    first_name: str
    last_name: str
    company_id: Union[uuid.UUID, None] = None
    recruiter_role: RecruiterRole = RecruiterRole.admin


class InviteToken(SQLModel):
    token: str
    email: str
    company_id: uuid.UUID
