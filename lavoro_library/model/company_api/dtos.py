import base64
import io
import uuid

from typing import Union

from pydantic import BaseModel, field_serializer, validator

from lavoro_library.model.company_api.db_models import RecruiterRole


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

    @field_serializer("logo")
    @classmethod
    def serialize_logo(cls, logo):
        if logo:
            encoded_file_content = base64.b64encode(logo).decode("utf-8")
            return encoded_file_content


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


class CreateRecruiterProfileWithCompanyDTO(BaseModel):
    first_name: str
    last_name: str
    company_id: Union[uuid.UUID, None] = None


class InviteTokenDTO(BaseModel):
    token: str
    email: str
    company_id: uuid.UUID
