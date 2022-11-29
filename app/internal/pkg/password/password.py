"""Module for crypt and decrypt password."""

import bcrypt
from pydantic import SecretBytes

__all__ = ["crypt_password", "check_password"]


def crypt_password(password: bytes) -> bytes:
    """Crypt password.

    Args:
        password: Raw password.

    Returns:
        Crypt password used bcrypt algorythm.
    """
    return bcrypt.hashpw(password, bcrypt.gensalt())


def check_password(password: SecretBytes, hashed: SecretBytes) -> bool:
    """Check equality of encrypted and raw password.

    Args:
        password: Raw password.
        hashed: Hashed password.

    Returns:
        True if equality check passed, False otherwise.
    """
    return bcrypt.checkpw(password.get_secret_value(), hashed.get_secret_value())
