"""Handle Postgresql Query Exceptions."""

from typing import Callable

import psycopg2
from psycopg2 import errorcodes

from app.pkg.models.base import Model
from app.pkg.models.exceptions.repository import DriverError, UniqueViolation

__all__ = ["handle_exception"]


def handle_exception(func: Callable[..., Model]):
    """Decorator Catching Postgresql Query Exceptions.

    Args:
        func: callable function object.

    Examples:
        For example, if you have a function that contains a query in postgresql,
        decorator ``handle_exception`` will catch the exceptions that can be
        raised by the query::

        >>> @handle_exception
        >>> async def get_user_by_id(user: User) -> User:
        ...    q = "SELECT * FROM users WHERE id = %(id)s"
        ...    return await db.fetch_one(q, values=user.dict())

    Returns:
        Result of call function.
    Raises:
        UniqueViolation: The query violates the domain uniqueness constraints
            of the database set.
        DriverError: Invalid database query/
    """

    async def wrapper(*args: object, **kwargs: object) -> Model:
        """Inner function. Catching Postgresql Query Exceptions.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Raises:
            UniqueViolation: The query violates the domain uniqueness constraints
                of the database set.
            DriverError: Invalid database query

        Returns:
            Result of call function.
        """

        try:
            return await func(*args, **kwargs)
        except psycopg2.Error as e:
            if e.pgcode == errorcodes.UNIQUE_VIOLATION:
                raise UniqueViolation

            raise DriverError(message=e.pgerror)

    return wrapper
