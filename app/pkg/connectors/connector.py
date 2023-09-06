"""Abstract connector.

Note:
    All connectors must be inherited by ``BaseConnector`` and implement its method.
"""

from abc import abstractmethod

__all__ = ["BaseConnector"]


class BaseConnector:
    """Abstract connector."""

    @abstractmethod
    async def get_connect(self, *args, **kwargs):
        """Getting connection pool in asynchronous."""

        try:
            _ = args, kwargs
        finally:
            raise NotImplementedError

    @abstractmethod
    async def close(self, *args, **kwargs):
        """Close connection."""

        raise NotImplementedError
