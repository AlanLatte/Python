"""Abstract connector."""

from abc import abstractmethod
from contextlib import asynccontextmanager

__all__ = ["BaseConnector"]


class BaseConnector:
    @abstractmethod
    def get_dsn(self) -> str:
        """Function for build DSN of connection."""

        raise NotImplementedError()

    @abstractmethod
    @asynccontextmanager
    async def get_connect(self):
        """Function for getting connection pool in async context."""

        raise NotImplementedError()
