"""MySql connector."""

from contextlib import asynccontextmanager

import aiomysql
import pydantic
from aiomysql import Connection, DictCursor

from .base_connector import BaseConnector

__all__ = ["Mysql"]


class Mysql(BaseConnector):
    username: str
    password: pydantic.SecretStr
    host: str
    port: pydantic.PositiveInt
    database_name: str

    def __init__(
        self,
        username: str,
        password: pydantic.SecretStr,
        host: str,
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
            f"aiomysql://"
            f"{self.username}:"
            f"{self.password.get_secret_value()}@"
            f"{self.host}:{self.port}/"
            f"{self.database_name}"
        )

    @asynccontextmanager
    async def get_connect(self) -> Connection:
        if self.pool is None:
            self.pool = await aiomysql.create_pool(
                host=self.host,
                port=self.port,
                user=self.username,
                password=self.password.get_secret_value(),
                db=self.database_name,
                cursorclass=DictCursor,
            )

        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                yield cur
                await conn.commit()
            conn.close()
