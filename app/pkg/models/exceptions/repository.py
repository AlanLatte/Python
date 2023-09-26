"""Exceptions for repository layer."""


from fastapi import status

from app.pkg.models.base import BaseAPIException

__all__ = [
    "UniqueViolation",
    "EmptyResult",
    "DriverError",
]


class UniqueViolation(BaseAPIException):
    message = "Not unique"
    status_code = status.HTTP_409_CONFLICT


class EmptyResult(BaseAPIException):
    message = "Empty result"
    status_code = status.HTTP_404_NOT_FOUND


class DriverError(BaseAPIException):
    """Exception for internal driver errors."""

    def __init__(self, message: str = None):
        """In case of message is None, a default message will be used."""
        if message:
            self.message = message

        super().__init__(message=message)

    message = "Internal driver error"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
