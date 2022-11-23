from typing import Optional

from fastapi import HTTPException
from app.pkg.models.types.strings import NotEmptyStr

__all__ = ["BaseAPIException"]


class BaseAPIException(HTTPException):
    # TODO: Добавить описание

    message: Optional[NotEmptyStr] = ...
    status_code: int = ...

    def __init__(self, message: Optional[NotEmptyStr] = None):
        if message is not None:
            self.message = message

        super().__init__(status_code=self.status_code, detail=self.message)
