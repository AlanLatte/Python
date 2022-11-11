__all__ = [
    "UniqueViolation",
    "EmptyResult",
    "DriverError",
    "ForeignKeyViolation",
    "CheckViolation",
    "NumericValueOutOfRange",
]

from fastapi import status

from app.pkg.models.base import BaseException


class UniqueViolation(BaseException):
    def __init__(self, message: str = "ForeignKeyViolation"):
        if message:
            self.message = message

    message = "Not unique"
    status_code = status.HTTP_409_CONFLICT


class EmptyResult(BaseException):
    message = "Empty result"
    status_code = status.HTTP_404_NOT_FOUND


class ForeignKeyViolation(BaseException):
    def __init__(self, message: str = "ForeignKeyViolation"):
        if message:
            self.message = message

    message = "Incorrect values"
    status_code = status.HTTP_400_BAD_REQUEST


class CheckViolation(BaseException):
    def __init__(self, message: str = None):
        if message:
            self.message = message

    message = "Incorrect values, check violation"
    status_code = status.HTTP_400_BAD_REQUEST


class NumericValueOutOfRange(BaseException):
    def __init__(self, message: str = None):
        if message:
            self.message = message

    message = "Incorrect values, too big"
    status_code = status.HTTP_400_BAD_REQUEST


class DriverError(BaseException):
    def __init__(self, message: str = None):
        if message:
            self.message = message

    message = "Internal driver error"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
