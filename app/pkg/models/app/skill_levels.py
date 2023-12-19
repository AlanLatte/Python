"""Models for skill level object."""

from pydantic.fields import Field
from pydantic.types import PositiveInt

from app.pkg.models.base import BaseModel

__all__ = [
    "SkillLevel",
    "CreateSkillLevelCommand",
    "ReadSkillLevelQuery",
    "UpdateSkillLevelCommand",
    "DeleteSkillLevelCommand",
]


class BaseSkillLevel(BaseModel):
    """Base model for skill levels."""


class SkillLevelFields:
    id: PositiveInt = Field(description="Internal skill level id.", example=1)
    level: PositiveInt = Field(description="Skill level.", example=1)
    description: str = Field(description="Skill level description.", example="Junior")


class _SkillLevel(BaseSkillLevel):
    level: PositiveInt = SkillLevelFields.level
    description: str = SkillLevelFields.description


class SkillLevel(_SkillLevel):
    id: PositiveInt = SkillLevelFields.id


# Commands.
class CreateSkillLevelCommand(_SkillLevel):
    ...


class UpdateSkillLevelCommand(_SkillLevel):
    id: PositiveInt = SkillLevelFields.id


class DeleteSkillLevelCommand(BaseSkillLevel):
    id: PositiveInt = SkillLevelFields.id


# Queries.
class ReadSkillLevelQuery(BaseSkillLevel):
    id: PositiveInt = SkillLevelFields.id
