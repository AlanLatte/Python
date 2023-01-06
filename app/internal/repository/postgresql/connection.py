from contextlib import asynccontextmanager

from aiopg.connection import Cursor
from dependency_injector.wiring import Provide, inject
from psycopg2.extras import RealDictCursor  # type: ignore

from app.pkg.connectors import Connectors
from app.pkg.connectors.postgresql import Postgresql

__all__ = ["get_connection"]


@asynccontextmanager
@inject
async def get_connection(
    postgresql: Postgresql = Provide[Connectors.postgresql],
) -> Cursor:
    """Get async connection to postgresql of pool."""

    async with postgresql.get_connect() as connection:
        async with (await connection.cursor(cursor_factory=RealDictCursor)) as cur:
            yield cur
