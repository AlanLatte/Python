"""Base exception for API."""

from typing import Optional, Union

from fastapi import HTTPException
from starlette import status

from app.pkg.models.types.strings import NotEmptyStr

__all__ = ["BaseAPIException"]


class BaseAPIException(HTTPException):
    """Base internal API Exception.

    Attributes:
        message: Message of exception.
        status_code: Status code of exception.

    Examples:
        Before use this class, you must create your own exception class.
        And inherit from this class.::
        >>> from app.pkg.models.base.exception import BaseAPIException
        >>> class MyException(BaseAPIException):
        ...     message = "My exception"
        ...     status_code = 400

        After that, you can use it in your code in some function runned under fastapi::
        >>> async def my_func():
        ...     raise MyException
    """

    # TODO: Добавить магическое слово, при определении которого, будет выбираться
    #       шаблон для формирования сообщения об ошибке.
    message: Optional[Union[NotEmptyStr, str]] = "Base API Exception"
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, message: Optional[NotEmptyStr] = None):
        if message is not None:
            self.message = message

        super().__init__(status_code=self.status_code, detail=self.message)
