import base64
import datetime
import uuid

from enum import Enum

from typing import List, Union

from pydantic import BaseModel, field_serializer

from lavoro_library.model.shared import Point


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


class JobPost(BaseModel):
    id: uuid.UUID
    company_id: uuid.UUID
    position_id: int
    description: str
    education_level_id: int
    skill_ids: List[int]
    work_type_id: int
    work_location: Point
    contract_type_id: int
    salary_min: Union[float, None] = None
    salary_max: Union[float, None] = None
    created_on_date: datetime
    last_updated_date: datetime
    end_date: datetime
    assignees: List[uuid.UUID] = []  # not part of the database model
