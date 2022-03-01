"""Base api exceptions."""

__all__ = ["BaseAPIException"]


class BaseAPIException(Exception):
    """Exception class for create determinate exception response from API."""

    #: str: Human readable string describing the exception.
    message: str
    #: int: Exception error code.
    status_code: int
