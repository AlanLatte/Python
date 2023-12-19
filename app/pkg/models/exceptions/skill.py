"""Exceptions for Skill model."""

from starlette import status

from app.pkg.models.base import BaseAPIException

__all__ = ["SkillNameAlreadyExists", "SkillNotFound"]


class SkillNameAlreadyExists(BaseAPIException):
    message = "This 'name' of skill already exists."
    status_code = status.HTTP_409_CONFLICT


class SkillNotFound(BaseAPIException):
    message = "Skill not found."
    status_code = status.HTTP_404_NOT_FOUND


__constrains__ = {
    "skills_name_key": SkillNameAlreadyExists,
}
