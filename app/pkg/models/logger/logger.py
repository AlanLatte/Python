from app.pkg.models.base import BaseEnum

__all__ = ["Logger"]


class Logger(str, BaseEnum):
    WARNING = "WARNING"
    INFO = "INFO"
    ERROR = "ERROR"
    DEBUG = "DEBUG"
    CRITICAL = "CRITICAL"
    NOTSET = "NOTSET"
