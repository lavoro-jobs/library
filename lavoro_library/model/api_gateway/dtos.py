import base64
import io
from typing import Union
from pydantic import BaseModel, validator


class PositionDTO(BaseModel):
    id: int
    position_name: str


class EducationLevelDTO(BaseModel):
    id: int
    education_level: str


class ContractTypeDTO(BaseModel):
    id: int
    contract_type: str


class WorkTypeDTO(BaseModel):
    id: int
    work_type: str


class SkillDTO(BaseModel):
    id: int
    skill_name: str


class JoinCompanyDTO(BaseModel):
    password: str
    first_name: str
    last_name: str
    profile_picture: Union[str, None] = None

    @validator("profile_picture")
    def check_properties(cls, profile_picture):
        if profile_picture:
            try:
                profile_picture_decoded = base64.b64decode(profile_picture)
            except Exception:
                raise ValueError("Invalid file")
            profile_picture_file = io.BytesIO(profile_picture_decoded)
            profile_picture_file.seek(0, io.SEEK_END)
            file_size = profile_picture_file.tell()
            if file_size > 3 * 1024 * 1024:
                raise ValueError("Profile picture file size must not exceed 3MB")
        return profile_picture
