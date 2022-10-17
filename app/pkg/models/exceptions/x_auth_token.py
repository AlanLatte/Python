from starlette import status

from app.pkg.models.base import BaseException

__all__ = ["InvalidCredentials"]


class InvalidCredentials(BaseException):
    message = "Could not validate credentials."
    status_code = status.HTTP_403_FORBIDDEN
