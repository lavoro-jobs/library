import inspect
import uuid

from datetime import datetime
from enum import Enum
from typing import Annotated, List, Union

from fastapi import Form
from pydantic import BaseModel, EmailStr, ValidationError, validator


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
    recruiter = "recruiter"


@as_form
class RegistrationForm(BaseModel):
    email: Annotated[EmailStr, Form()]
    password: Annotated[str, Form()]
    role: Annotated[Role, Form()]


@as_form
class LoginForm(BaseModel):
    grant_type: Annotated[Union[str, None], Form(pattern="password")] = None
    username: Annotated[str, Form()]
    password: Annotated[str, Form()]
    scope: Annotated[str, Form()] = ""
    client_id: Annotated[Union[str, None], Form()] = None
    client_secret: Annotated[Union[str, None], Form()] = None


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


class Point(BaseModel):
    longitude: float
    latitude: float

    @classmethod
    def from_string(cls, s: str):
        longitude, latitude = s.strip("()").split(",")
        return cls(x=float(longitude), y=float(latitude))


class Gender(str, Enum):
    male = "male"
    female = "female"
    other = "other"


class ApplicantProfileInDB(BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: str
    education_level_id: int
    age: int
    gender: Gender
    skills_id: List[int]
    account_id: uuid.UUID
    cv_url: str
    work_type_id: int
    seniority_level_id: int
    position_id: int
    home_location: Point
    work_location_max_distance: int
    contract_type_id: int
    min_salary: float

    @validator("home_location", pre=True)
    def parse_point(cls, value):
        if isinstance(value, str):
            return Point.from_string(value)
        elif isinstance(value, dict):
            return Point(**value)
        raise ValidationError(f"Invalid input for a Point: {value}")


class ExperienceInDB(BaseModel):
    id: uuid.UUID
    company_name: str
    position_id: int
    years: int
    applicant_profile_id: uuid.UUID


class Experience(BaseModel):
    id: uuid.UUID
    company_name: str
    position_id: int
    years: int


class CreateExperienceRequest(BaseModel):
    company_name: str
    position_id: int
    years: int


class CreateApplicantProfileRequest(BaseModel):
    first_name: str
    last_name: str
    education_level_id: int
    age: int
    gender: Gender
    skills_id: List[int]
    cv_url: str
    work_type_id: int
    seniority_level_id: int
    position_id: int
    home_location: Point
    work_location_max_distance: int
    contract_type_id: int
    min_salary: float
    experiences: List[CreateExperienceRequest] = []


class ApplicantProfile(ApplicantProfileInDB):
    experiences: List[Experience] = []
