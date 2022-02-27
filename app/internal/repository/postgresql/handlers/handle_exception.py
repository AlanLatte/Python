from typing import Callable

from psycopg2 import Error as QueryError
from psycopg2 import errorcodes

from app.pkg.models.base import Model
from app.pkg.models.exceptions.repository import DriverError, UniqueViolation

__all__ = ["handle_exception"]


def handle_exception(func: Callable[..., Model]):
    """Decorator Catching Postgresql Query Exceptions.

    Args:
        func: callable function object.

    Returns:
        Result of call function.
    Raises:
        UniqueViolation: The query violates the domain uniqueness constraints
            of the database set.
        DriverError: Invalid database query/
    """

    async def wrapper(*args: object, **kwargs: object) -> Model:
        try:
            return await func(*args, **kwargs)
        except QueryError as e:
            if e.pgcode == errorcodes.UNIQUE_VIOLATION:
                raise UniqueViolation

            raise DriverError(message=e.pgerror)

    return wrapper
