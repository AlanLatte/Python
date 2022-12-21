from pydantic import SecretBytes

from app.internal.pkg.password import password

__all__ = ["EncryptedSecretBytes"]


# TODO: Inherit from base custom type. ad-hoc overload __validate__ method
#   custom error handler in middlewares.
class EncryptedSecretBytes(SecretBytes):
    """Model for verify bytes range [6;256] and crypt than by bcrypt
    algorithm."""

    min_length = 6
    max_length = 256

    def crypt_password(self) -> None:
        self._secret_value = password.crypt_password(self.get_secret_value())
