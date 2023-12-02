import base64
import inspect
import uuid

from datetime import datetime
from enum import Enum
from typing import Annotated, List, Optional, Union

from fastapi import Form
from pydantic import BaseModel, EmailStr, field_serializer, model_validator


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


class Position(BaseModel):
    position_name: str


class PositionInDB(Position):
    id: int


class Education(BaseModel):
    education_level: str


class EducationInDB(Education):
    id: int


class ContractType(BaseModel):
    contract_type: str


class ContractTypeInDB(ContractType):
    id: int


class WorkType(BaseModel):
    work_type: str


class WorkTypeInDB(WorkType):
    id: int


class Skill(BaseModel):
    skill_name: str


class SkillInDB(Skill):
    id: int


class Point(BaseModel):
    longitude: float
    latitude: float

    @model_validator(mode="before")
    def parse_point_string(cls, data):
        if isinstance(data, str):
            # Assuming the format is "(longitude,latitude)"
            data = data.strip("()")
            longitude, latitude = map(float, data.split(","))
            return {"longitude": longitude, "latitude": latitude}
        return data


class Gender(str, Enum):
    male = "male"
    female = "female"
    other = "other"


class Experience(BaseModel):
    id: uuid.UUID
    company_name: str
    position_id: int
    years: int


class ApplicantProfile(BaseModel):
    first_name: str
    last_name: str
    education_level: str
    age: int
    gender: Gender
    skills: List[str]
    experiences: Optional[List[Experience]] = []
    work_type: str
    seniority_level: str  # TODO: add this catalog #PROJR-60
    position: str
    home_location: Point
    work_location_max_distance: int
    contract_type: str
    min_salary: float


class ApplicantProfileInDB(BaseModel):
    account_id: uuid.UUID
    first_name: str
    last_name: str
    education_level_id: int
    age: int
    gender: Gender
    skill_id_list: Optional[List[int]] = []
    experiences: Optional[List[Experience]] = []
    cv: Union[bytes, None] = None
    work_type_id: int
    seniority_level_id: int  # TODO: add this catalog #PROJR-60
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


class ExperienceInDB(BaseModel):
    id: uuid.UUID
    company_name: str
    position_id: int
    years: int
    applicant_profile_id: uuid.UUID


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
    skill_id_list: List[int]
    cv: Union[bytes, None] = None
    work_type_id: int
    seniority_level_id: int  # TODO: add this catalog #PROJR-60
    position_id: int
    home_location: Point
    work_location_max_distance: int
    contract_type_id: int
    min_salary: float
    experiences: List[CreateExperienceRequest] = []

    @field_serializer("cv")
    @classmethod
    def serialize_logo(cls, cv):
        if cv:
            encoded_file_content = base64.b64encode(cv).decode("utf-8")
            return encoded_file_content


class CreateCompanyRequest(BaseModel):
    name: str
    description: str
    logo: Union[bytes, None] = None

    @field_serializer("logo")
    @classmethod
    def serialize_logo(cls, logo):
        if logo:
            encoded_file_content = base64.b64encode(logo).decode("utf-8")
            return encoded_file_content


class CompanyInDB(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    logo: Union[bytes, None] = None

    @field_serializer("logo")
    @classmethod
    def serialize_logo(cls, logo):
        if logo:
            encoded_file_content = base64.b64encode(logo).decode("utf-8")
            return encoded_file_content


class Company(CompanyInDB):
    pass


class RecruiterRole(str, Enum):
    admin = "admin"
    employee = "employee"


class CreateRecruiterProfileRequest(BaseModel):
    first_name: str
    last_name: str
    company_id: Union[uuid.UUID, None] = None


class RecruiterProfileInDB(BaseModel):
    account_id: uuid.UUID
    first_name: str
    last_name: str
    company_id: Union[uuid.UUID, None] = None
    recruiter_role: RecruiterRole = RecruiterRole.admin


class RecruiterProfileWithCompanyName(BaseModel):
    first_name: str
    last_name: str
    company_name: Union[str, None] = None
    recruiter_role: RecruiterRole


class JoinCompanyRequest(BaseModel):
    password: str
    first_name: str
    last_name: str


class CompanyInvitation(BaseModel):
    token: str
    email: str
    company_id: uuid.UUID
