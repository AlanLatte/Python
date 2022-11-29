from pydantic import PositiveInt

from app.pkg.models.base import BaseModel
from app.pkg.models.types import NotEmptySecretStr

__all__ = [
    "JWTToken",
    "CreateJWTTokenCommand",
    "ReadJWTTokenQuery",
    "ReadJWTTokenQueryByFingerprint",
    "UpdateJWTTokenCommand",
    "DeleteJWTTokenCommand",
]


class JWTFields:
    ...


class BaseJWTToken(BaseModel):
    """Base class for refresh token."""


class JWTToken(BaseJWTToken):
    """RefreshToken from database."""

    user_id: PositiveInt
    refresh_token: NotEmptySecretStr
    fingerprint: NotEmptySecretStr


# Commands
class CreateJWTTokenCommand(BaseJWTToken):
    user_id: PositiveInt
    refresh_token: NotEmptySecretStr
    fingerprint: NotEmptySecretStr


class UpdateJWTTokenCommand(BaseJWTToken):
    user_id: PositiveInt
    refresh_token: NotEmptySecretStr
    fingerprint: NotEmptySecretStr


class DeleteJWTTokenCommand(BaseJWTToken):
    user_id: PositiveInt
    fingerprint: NotEmptySecretStr
    refresh_token: NotEmptySecretStr


# Queries
class ReadJWTTokenQuery(BaseJWTToken):
    user_id: PositiveInt
    refresh_token: NotEmptySecretStr


class ReadJWTTokenQueryByFingerprint(BaseJWTToken):
    user_id: PositiveInt
    fingerprint: NotEmptySecretStr
