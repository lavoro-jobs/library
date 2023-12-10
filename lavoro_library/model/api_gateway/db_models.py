from pydantic import BaseModel


class Position(BaseModel):
    id: int
    position_name: str


class EducationLevel(BaseModel):
    id: int
    education_level: str


class ContractType(BaseModel):
    id: int
    contract_type: str


class WorkType(BaseModel):
    id: int
    work_type: str


class Skill(BaseModel):
    id: int
    skill_name: str
