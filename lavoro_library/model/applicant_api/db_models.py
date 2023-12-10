import base64
import uuid

from enum import Enum
from typing import List, Union

from pydantic import BaseModel, field_serializer

from lavoro_library.model.shared import Point


class Gender(str, Enum):
    male = "male"
    female = "female"
    other = "other"


class Experience(BaseModel):
    id: uuid.UUID
    company_name: str
    position_id: int
    years: int
    applicant_account_id: uuid.UUID


class ApplicantProfile(BaseModel):
    account_id: uuid.UUID
    first_name: str
    last_name: str
    education_level_id: int
    age: int
    gender: Gender
    skill_ids: List[int]
    cv: Union[bytes, None] = None
    work_type_id: int
    seniority_level: int
    position_id: int
    home_location: Point
    work_location_max_distance: int
    contract_type_id: int
    min_salary: float

    @field_serializer("cv")
    @classmethod
    def serialize_cv(cls, cv):
        if cv:
            encoded_file_content = base64.b64encode(cv).decode("utf-8")
            return encoded_file_content
