"""Exceptions for auth module."""

from starlette import status

from app.pkg.models.base import BaseAPIException

__all__ = [
    "IncorrectLengthFingerprint",
    "IncorrectUsernameOrPassword",
]


class IncorrectLengthFingerprint(BaseAPIException):
    message = "Incorrect fingerprint"
    status_code = status.HTTP_400_BAD_REQUEST


class IncorrectUsernameOrPassword(BaseAPIException):
    message = "Incorrect username or password or secret key"
    status_code = status.HTTP_406_NOT_ACCEPTABLE
