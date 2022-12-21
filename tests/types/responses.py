import typing

import httpx

from app.pkg.models.base import BaseAPIException


class ErrorCheckerType(typing.Protocol):
    def __call__(
        self,
        response: httpx.Response,
        model: typing.Type[BaseAPIException],
        relative_occurrence: typing.Optional[bool] = False,
    ) -> bool:
        """Protocol of calling function in `router.responses:response_without_error`"""
