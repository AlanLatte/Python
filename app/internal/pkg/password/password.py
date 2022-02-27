import bcrypt
from pydantic import SecretBytes

__all__ = ["crypt_password", "check_password"]


def crypt_password(password: bytes) -> bytes:
    return bcrypt.hashpw(password, bcrypt.gensalt())


def check_password(password: SecretBytes, hashed: SecretBytes) -> bool:
    return bcrypt.checkpw(password.get_secret_value(), hashed.get_secret_value())

