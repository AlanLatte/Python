"""Package resource's module.

All resources should be inherited from :class:`.BaseAsyncResource`.
"""

from abc import abstractmethod
from typing import TypeVar

from dependency_injector import resources

__all__ = ["BaseAsyncResource"]


_T = TypeVar("_T")


class BaseAsyncResource(resources.AsyncResource):
    """Abstract base class for async resources."""

    @abstractmethod
    async def init(self, *args, **kwargs) -> _T:
        """Getting connection.

        Args:
            *args: Positional arguments for ``get_connect`` method.
            **kwargs: Keyword arguments for ``get_connect`` method.

        Examples:
            If you need a resource that will exist in a single instance, use
            ``Provide`` as usual::

                >>> from aiopg import Pool
                >>> from dependency_injector import containers, providers
                >>> from dependency_injector.wiring import Provide, inject
                >>>
                >>> from app.internal.repository.postgresql.connection import (
                ...     acquire_connection
                ... )
                >>> from app.pkg.connectors import Connectors
                >>>
                >>> class Container(containers.DeclarativeContainer):
                ...     connector: Connectors = providers.Container(Connectors)
                >>>
                >>> @inject
                ... async def auto_closed_pool(
                ...     psql: Pool = Provide[Container.connector.postgresql.connector],
                ... ):
                ...     async with acquire_connection(pool=psql) as cur:
                ...         await cur.execute("SELECT '1'")
                ...         return await cur.fetchone()

            If you need to automatically close the resource after the execution of the
            function - use ``Closing``::

                >>> import asyncio
                >>> from dependency_injector.wiring import Closing
                >>>
                >>> @inject
                ... async def native_closed_pool(
                ...     psql: Pool = Closing[
                ...         Provide[Container.connector.postgresql.connector]
                ...     ],
                ... ):
                ...     async with acquire_connection(pool=psql) as cur:
                ...         await cur.execute("SELECT '1'")
                ...         return await cur.fetchone()
        """

    @abstractmethod
    async def shutdown(self, resource: _T):
        """Close connection.

        Args:
            resource: Resource returned by :meth:`BaseAsyncResource.init()` method.

        Notes:
            You should implement ``close`` method of your connector here.
        """
