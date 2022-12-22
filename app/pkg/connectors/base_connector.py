"""Abstract connector.

Note:
    All connectors must be inherited by ``BaseConnector`` and implement its method.
"""

from abc import abstractmethod
from contextlib import asynccontextmanager

__all__ = ["BaseConnector"]


class BaseConnector:
    @abstractmethod
    def get_dsn(self) -> str:
        """Build DSN of connection."""

        raise NotImplementedError

    @abstractmethod
    @asynccontextmanager
    async def get_connect(self):
        """Getting connection pool in asynchronous context."""
        try:
            yield
        finally:
            raise NotImplementedError
