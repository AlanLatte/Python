from starlette.requests import Request
from starlette.responses import JSONResponse

from app.pkg.models.base import BaseAPIException


def handle_api_exceptions(request: Request, exc: BaseAPIException):
    """Handle all internal exceptions which inherited from `BaseAPIException`."""
    _ = request

    return JSONResponse(status_code=exc.status_code, content={"message": exc.message})
