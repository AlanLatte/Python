"""Secret bytes types for pydantic models."""

from typing import Any

from pydantic import SecretBytes
from pydantic.validators import bytes_validator

__all__ = ["EncryptedSecretBytes"]


# TODO: Inherit from base custom type. ad-hoc overload __validate__ method
#   custom error handler in middlewares.


class EncryptedSecretBytes(SecretBytes):
    """Model for verify bytes range [6;100] and crypt than by bcrypt
    algorithm."""

    min_length = 6
    max_length = 100

    def __repr__(self) -> str:
        return f"EncryptedSecretBytes(b'{self}')"

    @classmethod
    def validate(cls, value: Any) -> "EncryptedSecretBytes":
        if isinstance(value, cls):
            return value
        value = bytes_validator(value)
        return cls(value)
