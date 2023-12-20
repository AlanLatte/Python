"""Async resource for PostgresSQL connector."""

import aiopg

from app.pkg.connectors.resources import BaseAsyncResource

__all__ = ["Postgresql"]


class Postgresql(BaseAsyncResource):
    """PostgresSQL connector using aiopg."""

    async def init(self, dsn: str, *args, **kwargs) -> aiopg.Pool:
        """Getting connection pool in asynchronous.

        Args:
            dsn: D.S.N - Data Source Name.

        Returns:
            Created connection pool.
        """

        return await aiopg.create_pool(dsn=dsn, *args, **kwargs)

    async def shutdown(self, resource: aiopg.Pool):
        """Close connection.

        Args:
            resource: Resource returned by :meth:`.Postgresql.init()` method.

        Notes:
            This method is called automatically
            when the application is stopped
            or
            ``Closing`` provider is used.
        """

        resource.close()
        await resource.wait_closed()
