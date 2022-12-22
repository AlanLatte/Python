from pydantic import Field

from app.pkg.models.base import BaseModel
from app.pkg.models.types import EncryptedSecretBytes, NotEmptySecretStr
from app.pkg.models.user import UserFields
from app.pkg.models.user_role import UserRole

__all__ = ["Auth", "AuthCommand", "LogoutCommand"]


class AuthFields:
    access_token = Field(description="Bearer access token", example="exam.ple.token")
    refresh_token = Field(description="Bearer refresh token", example="exam.ple.token")
    fingerprint = Field(
        description="Unique fingerprint of user device",
        example="u-u-i-d",
    )
    role_name = UserFields.role_name
    username = UserFields.username
    password = UserFields.password


class BaseAuth(BaseModel):
    """Base model for auth."""


class Auth(BaseAuth):
    access_token: NotEmptySecretStr = AuthFields.access_token
    refresh_token: NotEmptySecretStr = AuthFields.refresh_token
    role_name: UserRole = AuthFields.role_name


class AuthCommand(BaseAuth):
    username: str = AuthFields.username
    password: EncryptedSecretBytes = AuthFields.password
    fingerprint: NotEmptySecretStr = AuthFields.fingerprint


class LogoutCommand(BaseAuth):
    username: str = AuthFields.username
    refresh_token: NotEmptySecretStr = AuthFields.refresh_token
