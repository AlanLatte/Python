"""Abstract connector.

Notes:
    All connectors must be inherited by :class:`.BaseConnector` and implement
        its method.
"""

from abc import abstractmethod

__all__ = ["BaseConnector"]


class BaseConnector:
    """Abstract connector."""

    @abstractmethod
    async def get_connect(self, *args, **kwargs):
        """Getting connection pool in asynchronous.

        Args:
            *args: Positional arguments for ``get_connect`` method.
            **kwargs: Keyword arguments for ``get_connect`` method.
        """

        raise NotImplementedError

    @abstractmethod
    async def close(self, *args, **kwargs):
        """Close connection."""

        raise NotImplementedError
