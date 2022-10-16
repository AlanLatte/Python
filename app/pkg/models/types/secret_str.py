from pydantic import SecretStr

__all__ = ["NotEmptySecretStr", "SecretToken"]


class NotEmptySecretStr(SecretStr):
    """Validate, that length of string is less or equal than 1."""

    min_length = 1


class SecretToken(SecretStr):
    min_length = 8
