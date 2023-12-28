from datetime import datetime
from typing import Union
from pydantic import BaseModel

from lavoro_library.model.applicant_api.dtos import ApplicantProfileForJobPostDTO
from lavoro_library.model.company_api.dtos import JobPostForApplicantDTO


class MatchDTO(BaseModel):
    job_post_id: str
    applicant_account_id: str
    match_score: float
    approved_by_applicant: bool = False
    created_on_date: datetime
    end_date: Union[datetime, None] = None


class ApplicantMatchDTO(BaseModel):
    job_post: JobPostForApplicantDTO
    match_score: float
    approved_by_applicant: Union[bool, None] = None
    created_on_date: datetime
    end_date: Union[datetime, None] = None


class JobPostMatchDTO(BaseModel):
    applicant_profile: ApplicantProfileForJobPostDTO
    match_score: float
    approved_by_applicant: Union[bool, None] = None
    created_on_date: datetime
    end_date: Union[datetime, None] = None


class ApplicationDTO(BaseModel):
    job_post_id: str
    applicant_account_id: str
    created_on_date: str
    approved_by_company: Union[bool, None] = None


class CreateCommentDTO(BaseModel):
    comment_body: str
