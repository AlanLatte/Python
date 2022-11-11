from typing import Optional, Type

from pydantic import SecretStr, validator

from app.pkg.models.base import BaseModel, Model
from app.pkg.models.exceptions.auth import IncorrectLengthFingerprint
from app.pkg.models.types import EncryptedSecretBytes, NotEmptySecretStr

__all__ = ["Auth", "AuthCommand"]

from app.pkg.models import UserRole


class BaseAuth(BaseModel):
    """Base model for auth."""


class Auth(BaseAuth):
    access_token: NotEmptySecretStr
    refresh_token: NotEmptySecretStr
    user_role_name: Optional[UserRole]


class AuthCommand(BaseAuth):
    username: str
    password: EncryptedSecretBytes
    fingerprint: NotEmptySecretStr
    verify_code: SecretStr

    @validator("fingerprint")
    def validate_min_length(
        cls: Type["Model"],
        value: NotEmptySecretStr,
    ) -> NotEmptySecretStr:
        min_length: int = 6
        if value.get_secret_value().__len__() < min_length:
            raise IncorrectLengthFingerprint
        return value
