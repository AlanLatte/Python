"""Base exception for API."""

from typing import Optional, Union

from fastapi import HTTPException
from starlette import status

from app.pkg.models.types.strings import NotEmptyStr

__all__ = ["BaseAPIException"]


class BaseAPIException(HTTPException):
    """Base internal API Exception.

    Attributes:
        message:
            Message of exception.
        status_code:
            Status code of exception.

    Examples:
        Before using this class, you must create your own exception class.
        And inherit from this class.::

            >>> from app.pkg.models.base.exception import BaseAPIException
            >>> from starlette import status
            >>> class MyException(BaseAPIException):
            ...     message = "My exception"
            ...     status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        After that, you can use it in your code in some function run under fastapi::

            >>> async def my_func():
            ...     raise MyException
    """

    # TODO: Добавить магическое слово, при определении которого, будет выбираться
    #       шаблон для формирования сообщения об ошибке.

    message: Optional[Union[NotEmptyStr, str]] = "Base API Exception"
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, message: Optional[Union[NotEmptyStr, str, Exception]] = None):
        """Init BaseAPIException.

        Args:
            message:
                Message of exception by default is "Base API Exception".
        """
        if message is not None:
            self.message = message

        if isinstance(message, Exception):
            self.message = str(message)

        super().__init__(status_code=self.status_code, detail=self.message)
