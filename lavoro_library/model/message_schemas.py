from datetime import datetime
import uuid
from typing import List, Union

from pydantic import BaseModel

from lavoro_library.model.shared import Point


class JobPostToMatch(BaseModel):
    job_post_id: uuid.UUID
    position_id: int
    education_level_id: int
    skill_ids: List[int]
    work_type_id: int
    work_location: Point
    contract_type_id: int
    salary_min: int
    salary_max: int
    seniority_level: int
    end_date: datetime


class ApplicantProfileToMatch(BaseModel):
    applicant_account_id: uuid.UUID
    education_level_id: int
    skill_ids: List[int]
    work_type_id: int
    seniority_level: int
    position_id: int
    home_location: Point
    work_location_max_distance: int
    contract_type_id: int
    min_salary: int
    experience_years: int


class DeleteJobPost(BaseModel):
    job_post_id: uuid.UUID


class ItemToMatch(BaseModel):
    data: Union[JobPostToMatch, ApplicantProfileToMatch, DeleteJobPost]


class MatchToCalculate(BaseModel):
    job_post_to_match: JobPostToMatch
    applicant_profile_to_match: ApplicantProfileToMatch
