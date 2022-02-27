from __future__ import annotations

from pydantic import SecretBytes
from app.internal.pkg.password import password

__all__ = ["EncryptedSecretBytes"]


class EncryptedSecretBytes(SecretBytes):
    min_length = 6
    max_length = 256

    def crypt_password(self) -> EncryptedSecretBytes:
        return EncryptedSecretBytes(password.crypt_password(self.get_secret_value()))
