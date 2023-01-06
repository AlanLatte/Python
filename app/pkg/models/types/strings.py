from __future__ import annotations

from typing import Dict, Optional

from pydantic import SecretStr
from pydantic.utils import update_not_none
from pydantic.validators import constr_length_validator

__all__ = ["NotEmptySecretStr", "NotEmptyStr"]


# TODO: Use generic pydantic model for create min and max range
class NotEmptySecretStr(SecretStr):
    """Validate, that length of string is less or equal than 1."""

    min_length = 1


class NotEmptyStr(str):
    """Validate, that length of string is less or equal than 1."""

    min_length: Optional[int] = 1
    max_length: Optional[int] = None

    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, str]) -> None:
        update_not_none(
            field_schema,
            type="string",
            writeOnly=False,
            minLength=cls.min_length,
            maxLength=cls.max_length,
        )

    @classmethod
    def __get_validators__(cls):
        yield constr_length_validator

    def __init__(self, value: str):
        self.value = value

    def __repr__(self) -> str:
        return f"NotEmptyStr('{self}')"
