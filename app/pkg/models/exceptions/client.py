from starlette import status

from app.pkg.models.base import BaseAPIException
from app.pkg.models.types.strings import NotEmptyStr

__all__ = ["BaseClientException", "BaseExternalClientException"]


class BaseClientException(BaseAPIException):
    def __init__(self, client_name: str):
        super(BaseClientException, self).__init__(
            message=NotEmptyStr(self.message.format(client_name)),
        )


class BaseExternalClientException(BaseClientException):
    message = "{} is not available now"
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
