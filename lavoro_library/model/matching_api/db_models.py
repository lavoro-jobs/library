from typing import Union
import uuid
from pydantic import BaseModel


class Match(BaseModel):
    job_post_id: uuid.UUID
    applicant_account_id: uuid.UUID
    match_score: float
    approved_by_applicant: Union[bool, None] = None
