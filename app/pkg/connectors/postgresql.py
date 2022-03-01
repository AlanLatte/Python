"""Postgresql connector."""

from contextlib import asynccontextmanager
from typing import Any, Dict
from aiopg import Connection
import pydantic

import aiopg

from .base_connector import BaseConnector

__all__ = ["Postgresql"]


class Postgresql(BaseConnector):
    """
    Attributes:
        username: username.
        password: password.
        host: host.
        port: port.
        database_name: database name.
    """
    settings: Dict[str, Any]

    def __init__(
        self,
        username: str,
        password: pydantic.SecretStr,
        host: pydantic.PositiveInt,
        port: pydantic.PositiveInt,
        database_name: str,
    ):
        """

        Args:
            username:
            password:
            host:
            port:
            database_name:
        """
        self.pool = None
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database_name = database_name

    def get_dsn(self):
        """Description of ``BaseConnector.get_dsn``."""
        return (
            f"postgresql://"
            f"{self.username}:"
            f"{self.password.get_secret_value()}@"
            f"{self.host}:{self.port}/"
            f"{self.database_name}"
        )

    @asynccontextmanager
    async def get_connect(self) -> Connection:
        """Create pool of connectors to a Postgres database.

        Yields:
            ``aiopg.Connection instance`` in asynchronous context manager.
        """
        if self.pool is None:
            self.pool = aiopg.create_pool(dsn=self.get_dsn())

        async with self.pool as pool:
            async with pool.acquire() as conn:
                yield conn
