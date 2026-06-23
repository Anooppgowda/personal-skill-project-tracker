from pydantic import BaseModel
from typing import List

class ProjectBase(BaseModel):
    title: str
    description: str

class ProjectCreate(ProjectBase):
    skill_id: int

class Project(ProjectBase):
    id: int
    skill_id: int

    class Config:
        from_attributes = True

class SkillBase(BaseModel):
    name: str
    level: str

class SkillCreate(SkillBase):
    pass

class Skill(SkillBase):
    id: int
    projects: List[Project] = []

    class Config:
        from_attributes = True