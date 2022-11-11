"""handlers that handle internal error raise and returns ``http json``
response.

Examples:
    For example, if in some level in code you raise error inherited by
    BaseException::

        ...  # exceptions.py
        class E(BaseException):
            status_code = status.HTTP_200_OK
            message = "test error."

        ...  # some_file.py
        async def some_internal_function():
            raise E

    When `some_internal_function` called, exception will process by
    ``handle_api_exceptions`` and returns json object::

        {
            "message": "test error."
        }
"""

from starlette.requests import Request
from starlette.responses import JSONResponse

from app.pkg.models.base import BaseException


def handle_api_exceptions(request: Request, exc: BaseException):
    """Handle all internal exceptions which inherited from `BaseException`."""
    _ = request

    return JSONResponse(status_code=exc.status_code, content={"message": exc.message})
