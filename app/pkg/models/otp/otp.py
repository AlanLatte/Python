# Command
from typing import Type

from pydantic import SecretStr, validator

from app.pkg.models.base import BaseModel, Model
from app.pkg.models.exceptions.auth import IncorrectLengthOTP

__all__ = ["Check2FACommand"]


class Check2FACommand(BaseModel):
    verify_code: SecretStr

    @validator("verify_code")
    def validate_min_length(
        cls: Type["Model"],
        value: SecretStr,
    ) -> SecretStr:
        length: int = 6
        if value.get_secret_value().__len__() != length:
            raise IncorrectLengthOTP
        return value
