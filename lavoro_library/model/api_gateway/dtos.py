from pydantic import BaseModel


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
