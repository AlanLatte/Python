"""Exceptions for direction model."""

from starlette import status

from app.pkg.models.base import BaseAPIException

__all__ = ["DirectionNameAlreadyExists", "DirectionNotFound"]


class DirectionNameAlreadyExists(BaseAPIException):
    message = "This 'name' of direction already exists."
    status_code = status.HTTP_409_CONFLICT


class DirectionNotFound(BaseAPIException):
    message = "Direction not found."
    status_code = status.HTTP_404_NOT_FOUND


__constrains__ = {
    "directions_name_key": DirectionNameAlreadyExists,
}
