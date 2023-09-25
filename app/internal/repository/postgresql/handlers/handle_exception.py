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
        func:
            callable function object.

    Examples:
        If you have a function that contains a query in postgresql,
        decorator :func:`.handle_exception` will catch the exceptions that can be
        raised by the query::

            >>> from app.pkg import models
            >>> from app.internal.repository.postgresql.connection import get_connection
            >>> @handle_exception
            ... async def create(self, cmd: models.CreateUserRoleCommand) -> None:
            ...     q = "insert into user_roles(role_name) values (%(role_name)s) on conflict do nothing returning role_name;"
            ...     async with get_connection() as cur:
            ...         await cur.execute(q, cmd.to_dict(show_secrets=True))

    Returns:
        Result of call function.

    Raises:
        UniqueViolation: The query violates the domain uniqueness constraints
            of the database set.
        DriverError: Any error during execution query on a database.
    """

    async def wrapper(*args: object, **kwargs: object) -> Model:
        """Inner function. Catching Postgresql Query Exceptions.

        Args:
            *args:
                Positional arguments.
            **kwargs:
                Keyword arguments.

        Raises:
            UniqueViolation: The query violates the domain uniqueness constraints
                of the database set.
            DriverError: Any error during execution query on an database.

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
