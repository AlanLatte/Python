import typing
from contextlib import asynccontextmanager
from pathlib import Path

import aiosqlite

from app.pkg.connectors.base_connector import BaseConnector

__all__ = ["SQLite"]


class SQLite(BaseConnector):
    sqlite_path: Path
    connection: typing.Optional[aiosqlite.Connection] = None

    def __init__(self, sqlite_path: Path):
        self.connection = None
        self.sqlite_path = sqlite_path

    def get_dsn(self):
        return f"sqlite:///{self.sqlite_path.absolute()}"

    @asynccontextmanager
    async def get_connect(self):
        """Connect to a Postgres database."""
        if self.connection is None:
            self.connection = aiosqlite.connect(database=self.sqlite_path)

        async with self.connection as conn:
            yield conn
