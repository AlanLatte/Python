"""All enum inside models must be inherited by :class:`.BaseEnum`"""

from enum import Enum

__all__ = ["BaseEnum"]


class BaseEnum(Enum):
    """Base ENUM model."""

    def __repr__(self) -> str:
        """Return string representation of enum value."""

        return self.__str__()

    def __str__(self) -> str:
        """Return string representation of enum value."""

        return str(self.value)
