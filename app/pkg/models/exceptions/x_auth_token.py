from starlette import status

from app.pkg.models.base import BaseAPIException

__all__ = ["InvalidCredentials"]


class InvalidCredentials(BaseAPIException):
    message = "Could not validate credentials."
    status_code = status.HTTP_403_FORBIDDEN
