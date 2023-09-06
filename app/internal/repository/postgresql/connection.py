from contextlib import asynccontextmanager
from typing import Optional, Union

from aiopg import Pool
from aiopg.pool import Cursor
from dependency_injector.wiring import Provide, inject
from psycopg2.extensions import cursor  # type: ignore
from psycopg2.extras import RealDictCursor  # type: ignore

from app.pkg.connectors import Connectors

__all__ = ["get_connection", "acquire_connection"]


@asynccontextmanager
@inject
async def get_connection(
    pool: Pool = Provide[Connectors.postgresql.connector],
    return_pool: bool = False,
) -> Union[Cursor, Pool]:
    """Get async pool to postgresql of pool.

    Args:
        pool: postgresql pool.
        return_pool: if True, return pool, else return connection.

    Examples:
        For example, if you have a function that contains a query in postgresql,
        context manager ``get_connection`` will get async connection to postgresql
        of pool::
        >>> from app.internal.repository.postgresql.connection import get_connection
        >>> async def exec_some_sql_function() -> None:
        ...     async with get_connection() as c:
        ...         await c.execute("SELECT * FROM users")

    Returns:
        Async connection to postgresql.
    """

    if not isinstance(pool, Pool):
        pool = await pool

    if return_pool:
        yield pool
        return

    async with acquire_connection(pool=pool, cursor_factory=None) as cur:
        yield cur


@asynccontextmanager
async def acquire_connection(
    pool: Pool,
    cursor_factory: Optional[cursor] = None,
) -> Cursor:
    """Acquire connection from pool.

    Args:
        pool: postgresql pool.
        cursor_factory: cursor factory.

    Examples:
        For example, if you have a function that contains a query in postgresql,
        context manager ``acquire_connection`` will get async connection to postgresql
        of pool::
        >>> from app.internal.repository.postgresql import connection
        >>> async def exec_some_sql_function() -> None:
        ...     q = "select * from users;"
        ...     async with connection.get_connection(return_pool=True) as __pool:
        ...         async with connection.acquire_connection(__pool) as _cursor:
        ...             await _cursor.execute(q)
        ...         async with connection.acquire_connection(__pool) as _cursor:
        ...             await _cursor.execute(q)

    Returns:
        Async connection to postgresql.
    """

    if cursor_factory is None:
        cursor_factory = RealDictCursor

    async with pool.acquire() as conn:
        __cursor = await conn.cursor(cursor_factory=cursor_factory)
        yield __cursor
