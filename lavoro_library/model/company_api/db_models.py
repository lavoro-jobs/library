import base64
import uuid

from enum import Enum

from typing import Union

from pydantic import BaseModel, field_serializer


class RecruiterRole(str, Enum):
    admin = "admin"
    employee = "employee"


class Company(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    logo: Union[bytes, str, None] = None

    @field_serializer("logo")
    @classmethod
    def serialize_logo(cls, logo):
        if logo:
            if isinstance(logo, str):
                return logo
            else:
                return base64.b64encode(logo).decode("utf-8")
        else:
            return None


class RecruiterProfile(BaseModel):
    account_id: uuid.UUID
    company_id: uuid.UUID
    first_name: str
    last_name: str
    company_id: Union[uuid.UUID, None] = None
    recruiter_role: RecruiterRole = RecruiterRole.admin


class InviteToken(BaseModel):
    token: str
    email: str
    company_id: uuid.UUID
