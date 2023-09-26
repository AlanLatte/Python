"""Authentication middleware for token-based authentication."""

from fastapi import Security
from fastapi.security import APIKeyHeader

from app.pkg.models.exceptions.token_verification import InvalidCredentials
from app.pkg.settings import settings

__all__ = ["token_based_verification"]

x_api_key_header = APIKeyHeader(name="X-ACCESS-TOKEN")


# TODO: Add X_API_TOKEN to settings
async def token_based_verification(
    api_key_header: str = Security(x_api_key_header),
):
    """This function is used for routers that need to be protected by token-
    based authentication.

    Notes:
        Token for access to API is X-ACCESS-TOKEN from header and gets from
        :attr:`.Settings.API.X_ACCESS_TOKEN`.

    Args:
        api_key_header:
            X-ACCESS-TOKEN from header.

    Examples:
        You can use this function in your specific router like this::

            >>> from fastapi import APIRouter, Depends
            >>>
            >>> from app.internal.pkg.middlewares.token_based_verification import (
            ...     token_based_verification
            ... )
            >>>
            >>> router = APIRouter(dependencies=[Depends(token_based_verification)])
            >>>
            >>> @router.get("/test")
            ... async def test():
            ...     return {"message": "Hello World!"}

        Or you can use token-based authentication in your global point of application in
        :func:`.create_app` function like this::

            >>> from fastapi import FastAPI
            >>> app = FastAPI(dependencies=[Depends(token_based_verification)])

    Raises:
        InvalidCredentials:
            If X-ACCESS-TOKEN from header not equal X_ACCESS_TOKEN from settings.

    See Also: https://fastapi.tiangolo.com/tutorial/security/first-steps/

    Returns:
        None
    """
    value = settings.API.X_ACCESS_TOKEN.get_secret_value()
    if api_key_header != value:
        raise InvalidCredentials
