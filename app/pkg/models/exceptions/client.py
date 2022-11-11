from starlette import status

from app.pkg.models.base import BaseException


class BaseClientException(BaseException):
    ...


class ClientException(BaseClientException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
