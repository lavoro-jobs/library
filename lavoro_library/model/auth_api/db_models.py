import uuid

from datetime import datetime
from enum import Enum

from sqlmodel import SQLModel


class Role(str, Enum):
    applicant = "applicant"
    recruiter = "recruiter"


class Account(SQLModel):
    id: uuid.UUID
    email: str
    password_hash: str
    is_active: bool
    role: str
    created_on: datetime


class VerificationToken(SQLModel):
    token: str
    account_id: uuid.UUID
    expiry_date: datetime
