"""Base api exceptions."""

__all__ = ["BaseAPIException"]


class BaseAPIException(Exception):
    message: str
    status_code: int
