from sqlmodel import SQLModel


class Position(SQLModel):
    id: int
    position_name: str


class EducationLevel(SQLModel):
    id: int
    education_level: str


class ContractType(SQLModel):
    id: int
    contract_type: str


class WorkType(SQLModel):
    id: int
    work_type: str


class Skill(SQLModel):
    id: int
    skill_name: str
