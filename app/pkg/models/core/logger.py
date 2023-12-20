"""LoggerLevel model."""

from app.pkg.models.base import BaseEnum

__all__ = ["LoggerLevel"]


class LoggerLevel(str, BaseEnum):
    WARNING = "WARNING"
    INFO = "INFO"
    ERROR = "ERROR"
    DEBUG = "DEBUG"
    CRITICAL = "CRITICAL"
    NOTSET = "NOTSET"
