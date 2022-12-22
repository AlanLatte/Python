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
    def __init__(self, message: str = None):
        if message:
            self.message = message

    message = "Internal driver error"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
