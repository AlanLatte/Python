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
    value = settings.X_API_TOKEN.get_secret_value()
    if api_key_header != value:
        raise InvalidCredentials
