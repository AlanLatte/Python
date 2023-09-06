from abc import abstractmethod
from typing import TypeVar

from dependency_injector import resources

__all__ = ["BaseAsyncResource"]


T = TypeVar("T")


class BaseAsyncResource(resources.AsyncResource):
    @abstractmethod
    async def init(self, *args, **kwargs) -> T:
        """Getting connection.

        Args:
            *args: Positional arguments for ``get_connect`` method.
            **kwargs: Keyword arguments for ``get_connect`` method.
        """

    @abstractmethod
    async def shutdown(self, connector: T):
        """Close connection.

        Args:
            connector: Resource returned by ``init`` method.

        Notes:
            You should implement ``close`` method in your connector here
        """
