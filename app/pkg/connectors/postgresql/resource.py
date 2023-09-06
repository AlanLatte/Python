import aiopg

from app.pkg.connectors.resourсes import BaseAsyncResource

__all__ = ["Postgresql"]


class Postgresql(BaseAsyncResource):
    """PostgreSQL connector using aiopg."""

    async def init(self, dsn: str, *args, **kwargs) -> aiopg.Pool:
        """Getting connection pool in asynchronous.

        Args:
            dsn: Data Source Name.

        Returns:
            Created connection pool.
        """

        return await aiopg.create_pool(dsn=dsn, *args, **kwargs)

    async def shutdown(self, connector: aiopg.Pool):
        """Close connection.

        Args:
            connector: Resource returned by ``init`` method.

        Notes:
            This method is called automatically when the application is stopped.
        """

        connector.close()
        await connector.wait_closed()
