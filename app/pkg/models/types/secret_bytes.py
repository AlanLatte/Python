from typing import Any

from pydantic import SecretBytes, ValidationError
from pydantic.validators import bytes_validator

from app.internal.pkg.password import password

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
        """Validate bytes range [6;256] and crypt than by bcrypt"""

        if isinstance(value, cls):
            return value
        value = bytes_validator(value)
        return cls(value)

    def crypt_password(self) -> None:
        self._secret_value = password.crypt_password(self.get_secret_value())
