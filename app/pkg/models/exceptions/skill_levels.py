"""Exceptions for SkillLevel model."""

from starlette import status

from app.pkg.models.base import BaseAPIException

__all__ = ["SkillLevelAlreadyExists", "SkillLevelNotFound"]


class SkillLevelAlreadyExists(BaseAPIException):
    message = "This 'level' already exists."
    status_code = status.HTTP_409_CONFLICT


class SkillLevelNotFound(BaseAPIException):
    message = "Skill level not found."
    status_code = status.HTTP_404_NOT_FOUND


__constrains__ = {
    "skill_levels_level_key": SkillLevelAlreadyExists,
}
