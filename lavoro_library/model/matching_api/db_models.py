from datetime import datetime
from typing import Union
import uuid
from pydantic import BaseModel


class Match(BaseModel):
    job_post_id: uuid.UUID
    applicant_account_id: uuid.UUID
    match_score: float
    approved_by_applicant: Union[bool, None] = None
    created_on_date: datetime
    end_date: Union[datetime, None] = None


class Application(BaseModel):
    job_post_id: uuid.UUID
    applicant_account_id: uuid.UUID
    created_on_date: datetime
    approved_by_company: Union[bool, None] = None


class Comment(BaseModel):
    account_id: uuid.UUID
    job_post_id: uuid.UUID
    applicant_account_id: uuid.UUID
    comment_body: str
    created_on_date: datetime
