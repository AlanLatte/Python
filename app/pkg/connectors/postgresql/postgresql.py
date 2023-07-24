"""Postgresql connector."""

import typing

import aiopg
from aiopg import Pool

from app.pkg.connectors.connector import BaseConnector

__all__ = ["Postgresql"]


class Postgresql(BaseConnector):
    """Postgresql connector."""

    __pool: typing.Optional[Pool] = None

    dsn: typing.Optional[str] = None

    def __init__(self, postgres_dsn: str):
        """Settings for create postgresql dsn.

        Args:
            postgres_dsn: postgresql dsn for connect to database.
        """

        self.dsn = postgres_dsn

    async def get_connect(self, *args, **kwargs) -> Pool:
        """Create pool of connectors to a Postgres database.

        Returns:
            ``aiopg.Connection instance`` in asynchronous context manager.
        """

        if self.__pool is None:
            self.__pool = await aiopg.create_pool(dsn=self.dsn, *args, **kwargs)

        return self.__pool

    async def close(self, *args, **kwargs):
        """Close pool to database."""

        if self.__pool is None:
            raise ValueError("Pool is not initialized")

        self.__pool.close()
        await self.__pool.wait_closed()
