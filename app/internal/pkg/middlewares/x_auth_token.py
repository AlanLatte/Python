from fastapi import Security
from fastapi.security import APIKeyHeader

from app.pkg.models.exceptions.x_auth_token import InvalidCredentials
from app.pkg.settings import settings

__all__ = ["get_x_token_key"]

x_api_key_header = APIKeyHeader(name="X-ACCESS-TOKEN")


# TODO: Add X_API_TOKEN to settings
async def get_x_token_key(
    api_key_header: str = Security(x_api_key_header),
):
    """Get X-ACCESS-TOKEN from header and compare it with X_API_TOKEN from
    settings.

    This function is used for authentication.

    Args:
        api_key_header: X-ACCESS-TOKEN from header.

    Raises:
        InvalidCredentials: If X-ACCESS-TOKEN from header not equal
            X_API_TOKEN from settings.


    See Also: https://fastapi.tiangolo.com/tutorial/security/api-keys/

    Returns: None
    """
    value = settings.API.X_ACCESS_TOKEN.get_secret_value()
    if api_key_header != value:
        raise InvalidCredentials
