"""Postgresql connector."""

from contextlib import asynccontextmanager
from typing import Any, Dict
import pydantic

import aiopg

__all__ = ["Postgresql"]


class Postgresql:
    settings: Dict[str, Any]

    def __init__(
        self,
        username: str,
        password: pydantic.SecretStr,
        host: pydantic.PositiveInt,
        port: pydantic.PositiveInt,
        database_name: str,
    ):
        self.pool = None
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database_name = database_name

    def get_dsn(self):
        return (
            f"postgresql://"
            f"{self.username}:"
            f"{self.password.get_secret_value()}@"
            f"{self.host}:{self.port}/"
            f"{self.database_name}"
        )

    @asynccontextmanager
    async def get_connect(self):
        """Connect to a Postgres database."""
        if self.pool is None:
            self.pool = aiopg.create_pool(dsn=self.get_dsn())

        async with self.pool as pool:
            async with pool.acquire() as conn:
                yield conn
