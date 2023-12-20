"""Recursive attribute access and setting."""

from functools import reduce
from typing import TypeVar

__all__ = ["rec_getattr", "rec_setattr"]

_T = TypeVar("_T")


def rec_getattr(obj: object, attr: str) -> _T:
    """Recursively access an attribute of an object.

    Args:
        obj: Object to access.
        attr: Attribute to access.

    Examples:
        ::

            >>> class A:
            ...     class B:
            ...         class C:
            ...             attr = 1
            >>> rec_getattr(A, "B.C.attr")
            1

    Returns:
        Attribute of an object.
    """
    return reduce(getattr, attr.split("."), obj)


def rec_setattr(obj: object, attr: str, value: _T) -> None:
    """Recursively set an attribute of an object.

    Args:
        obj: Object to access.
        attr: Attribute to access.
        value: Value to set.

    Examples:
        ::

            >>> class A:
            ...     class B:
            ...         class C:
            ...             attr = 1
            >>> rec_setattr(A, "B.C.attr", 2)
            >>> rec_getattr(A, "B.C.attr")
            2

    Returns:
        None
    """

    attrs = attr.split(".")
    setattr(reduce(getattr, attrs[:-1], obj), attrs[-1], value)
