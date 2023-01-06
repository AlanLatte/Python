"""Postgresql connector."""
import typing
import urllib.parse
from contextlib import asynccontextmanager

import aiopg
import pydantic
from aiopg import Connection

from .base_connector import BaseConnector

__all__ = ["Postgresql"]


class Postgresql(BaseConnector):
    username: str
    password: pydantic.SecretStr
    host: pydantic.PositiveInt
    port: pydantic.PositiveInt
    database_name: str
    pool: typing.Optional[typing.AsyncContextManager[aiopg.Pool]] = None

    def __init__(
        self,
        username: str,
        password: pydantic.SecretStr,
        host: pydantic.PositiveInt,
        port: pydantic.PositiveInt,
        database_name: str,
    ):
        """Settings for create postgresql dsn.

        Args:
            username: database username.
            password: database password.
            host: the host where the database is located.
            port: the port of database server.
            database_name: database name.
        """
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database_name = database_name

    def get_dsn(self) -> str:
        """Description of ``BaseConnector.get_dsn``."""
        return (
            f"postgresql://"
            f"{self.username}:"
            f"{urllib.parse.quote_plus(self.password.get_secret_value())}@"
            f"{self.host}:{self.port}/"
            f"{self.database_name}"
        )

    @asynccontextmanager
    async def get_connect(self) -> typing.AsyncIterator[Connection]:
        """Create pool of connectors to a Postgres database.

        Yields:
            ``aiopg.Connection instance`` in asynchronous context manager.
        """
        if self.pool is None:
            self.pool = aiopg.create_pool(dsn=self.get_dsn())

        async with self.pool as pool:
            async with pool.acquire() as conn:
                yield conn
