"""Models for direction object."""

import typing

from pydantic.fields import Field
from pydantic.types import PositiveInt

from app.pkg.models.base import BaseModel

__all__ = [
    "Direction",
    "CreateDirectionCommand",
    "ReadDirectionQuery",
    "ReadAllDirectionByIdQuery",
    "UpdateDirectionCommand",
    "DeleteDirectionCommand",
]


class BaseDirection(BaseModel):
    """Base model for directions."""


class DirectionFields:
    id: PositiveInt = Field(description="Internal direction id.", example=1)
    ids: typing.List[PositiveInt] = Field(
        description="Internal direction ids.",
        example=[1, 2],
    )
    name: str = Field(description="Direction name.", example="Backend")


class _Direction(BaseDirection):
    name: str = DirectionFields.name


class Direction(_Direction):
    id: PositiveInt = DirectionFields.id


# Commands.
class CreateDirectionCommand(_Direction):
    ...


class UpdateDirectionCommand(_Direction):
    id: PositiveInt = DirectionFields.id


class DeleteDirectionCommand(BaseDirection):
    id: PositiveInt = DirectionFields.id


# Queries.
class ReadDirectionQuery(BaseDirection):
    id: PositiveInt = DirectionFields.id


class ReadAllDirectionByIdQuery(BaseDirection):
    ids: typing.List[PositiveInt] = DirectionFields.ids
