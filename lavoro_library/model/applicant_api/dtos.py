import base64
import io
import uuid

from pydantic import BaseModel, validator
from typing import List, Union

from lavoro_library.model.api_gateway.dtos import (
    ContractTypeDTO,
    EducationLevelDTO,
    PositionDTO,
    SkillDTO,
    WorkTypeDTO,
)
from lavoro_library.model.applicant_api.db_models import Gender
from lavoro_library.model.shared import Point


class ExperienceDTO(BaseModel):
    id: uuid.UUID
    company_name: str
    position: PositionDTO
    years: int


class ApplicantProfileDTO(BaseModel):
    first_name: str
    last_name: str
    education_level: EducationLevelDTO
    age: int
    gender: Gender
    skills: List[SkillDTO]
    experiences: List[ExperienceDTO] = []
    cv: Union[str, None] = None
    work_type: WorkTypeDTO
    seniority_level: int
    position: PositionDTO
    home_location: Point
    work_location_max_distance: int
    contract_type: ContractTypeDTO
    min_salary: float


class CreateExperienceDTO(BaseModel):
    company_name: str
    position_id: int
    years: int


class CreateApplicantProfileDTO(BaseModel):
    first_name: str
    last_name: str
    education_level_id: int
    age: int
    gender: Gender
    skill_ids: List[int] = []
    cv: Union[str, None] = None
    work_type_id: int
    seniority_level: int
    position_id: int
    home_location: Point
    work_location_max_distance: int
    contract_type_id: int
    min_salary: float

    @validator("cv")
    def check_properties(cls, cv):
        if cv:
            try:
                cv_decoded = base64.b64decode(cv)
            except Exception:
                raise ValueError("Invalid file")
            cv_file = io.BytesIO(cv_decoded)
            cv_file.seek(0, io.SEEK_END)
            file_size = cv_file.tell()
            if file_size > 2 * 1024 * 1024:
                raise ValueError("CV file size must not exceed 2MB")
        return cv


class CreateApplicantProfileWithExperiencesDTO(CreateApplicantProfileDTO):
    experiences: List[CreateExperienceDTO] = []


class UpdateApplicantProfileDTO(BaseModel):
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    education_level_id: Union[int, None] = None
    age: Union[int, None] = None
    gender: Union[Gender, None] = None
    skill_ids: Union[List[int], None] = None
    cv: Union[str, None] = None
    work_type_id: Union[int, None] = None
    seniority_level: Union[int, None] = None
    position_id: Union[int, None] = None
    home_location: Union[Point, None] = None
    work_location_max_distance: Union[int, None] = None
    contract_type_id: Union[int, None] = None
    min_salary: Union[float, None] = None

    @validator("cv")
    def check_properties(cls, cv):
        if cv:
            try:
                cv_decoded = base64.b64decode(cv)
            except Exception:
                raise ValueError("Invalid file")
            cv_file = io.BytesIO(cv_decoded)
            cv_file.seek(0, io.SEEK_END)
            file_size = cv_file.tell()
            if file_size > 2 * 1024 * 1024:
                raise ValueError("CV file size must not exceed 2MB")
        return cv


class UpdateApplicantExperienceDTO(BaseModel):
    company_name: Union[str, None] = None
    position_id: Union[int, None] = None
    years: Union[int, None] = None
