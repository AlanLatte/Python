"""Models fot student skills."""

import typing

from pydantic.fields import Field
from pydantic.types import PositiveInt

from app.pkg.models.base import BaseModel

__all__ = [
    "Skill",
    "CreateSkillCommand",
    "ReadSkillQuery",
    "ReadAllSkillByIdQuery",
    "UpdateSkillCommand",
    "DeleteSkillCommand",
]


class BaseSkill(BaseModel):
    """Base model for skills."""


class SkillFields:
    id: PositiveInt = Field(description="Internal skill id.", example=1)
    ids: typing.List[PositiveInt] = Field(
        description="List of skill ids.",
        example=[1, 2, 3],
    )
    name: str = Field(description="Skill name.", example="Python")


class _Skill(BaseSkill):
    name: str = SkillFields.name


class Skill(_Skill):
    id: PositiveInt = SkillFields.id


# Commands.
class CreateSkillCommand(_Skill):
    ...


class UpdateSkillCommand(_Skill):
    id: PositiveInt = SkillFields.id


class DeleteSkillCommand(BaseSkill):
    id: PositiveInt = SkillFields.id


# Queries.
class ReadSkillQuery(BaseSkill):
    id: PositiveInt = SkillFields.id


class ReadAllSkillByIdQuery(BaseSkill):
    ids: typing.List[PositiveInt] = SkillFields.ids
