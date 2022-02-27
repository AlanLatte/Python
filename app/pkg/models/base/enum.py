"""All enum inside models must be inherited by `BaseEnum`"""
from enum import Enum

__all__ = ["BaseEnum"]


class BaseEnum(Enum):
    """Base ENUM model."""

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.value)
