import base64
import io
import uuid

from datetime import datetime, timezone
from typing import List, Union

from pydantic import BaseModel, field_serializer, validator
from lavoro_library.model.api_gateway.dtos import ContractTypeDTO, EducationLevelDTO, PositionDTO, SkillDTO, WorkTypeDTO

from lavoro_library.model.company_api.db_models import RecruiterRole
from lavoro_library.model.shared import Point


class RecruiterProfileDTO(BaseModel):  # RecruiterProfileWithCompanyName
    first_name: str
    last_name: str
    company_id: Union[uuid.UUID, None] = None
    recruiter_role: RecruiterRole


class RecruiterProfileWithCompanyNameDTO(BaseModel):
    first_name: str
    last_name: str
    company_name: Union[str, None] = None
    recruiter_role: RecruiterRole


class CompanyDTO(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    logo: Union[str, None] = None

    @validator("logo")
    def check_properties(cls, logo):
        if logo:
            try:
                logo_decoded = base64.b64decode(logo)
            except Exception:
                raise ValueError("Invalid file")
            logo_file = io.BytesIO(logo_decoded)
            logo_file.seek(0, io.SEEK_END)
            file_size = logo_file.tell()
            if file_size > 2 * 1024 * 1024:
                raise ValueError("Logo file size must not exceed 2MB")
        return logo


class CreateCompanyDTO(BaseModel):
    name: str
    description: str
    logo: Union[str, None] = None

    @validator("logo")
    def check_properties(cls, logo):
        if logo:
            try:
                logo_decoded = base64.b64decode(logo)
            except Exception:
                raise ValueError("Invalid file")
            logo_file = io.BytesIO(logo_decoded)
            logo_file.seek(0, io.SEEK_END)
            file_size = logo_file.tell()
            if file_size > 2 * 1024 * 1024:
                raise ValueError("Logo file size must not exceed 2MB")
        return logo


class CreateRecruiterProfileDTO(BaseModel):
    first_name: str
    last_name: str
    company_id: Union[uuid.UUID, None] = None


class InviteTokenDTO(BaseModel):
    token: str
    email: str
    company_id: uuid.UUID


class JobPostDTO(BaseModel):
    id: uuid.UUID
    position: PositionDTO
    description: str
    education_level: EducationLevelDTO
    skills: List[SkillDTO]
    work_type: WorkTypeDTO
    work_location: Point
    contract_type: ContractTypeDTO
    salary_min: Union[float, None] = None
    salary_max: Union[float, None] = None
    end_date: datetime
    assignees: List[uuid.UUID] = []


class CreateJobPostDTO(BaseModel):
    position_id: int
    description: str
    education_level_id: int
    skill_ids: List[int]
    work_type_id: int
    work_location: Point
    contract_type_id: int
    salary_min: Union[float, None] = None
    salary_max: Union[float, None] = None
    end_date: datetime
    assignees: Union[List[uuid.UUID], None] = []

    @validator("end_date")
    def check_end_date(cls, end_date):
        if end_date < datetime.now(timezone.utc):
            raise ValueError("End date must be in the future")
        return end_date

    @validator("salary_min")
    def check_salary_min(cls, salary_min):
        if salary_min and salary_min <= 0:
            raise ValueError("Salary min must be greater than 0")
        return salary_min

    @validator("salary_max")
    def check_salary_max(cls, salary_max, values):
        if salary_max:
            if salary_max <= 0:
                raise ValueError("Salary max must be greater than 0")
            if values.get("salary_min"):
                if salary_max < values["salary_min"]:
                    raise ValueError("Salary max must be greater than salary min")
        return salary_max

    @validator("assignees")
    def check_assignees(cls, assignees):
        if len(set(assignees)) != len(assignees):
            raise ValueError("Assignees must be unique")
        return assignees
