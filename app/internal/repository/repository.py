"""Abstract repository interface."""

from abc import ABC
from typing import List, TypeVar

from app.pkg.models.base import Model

__all__ = ["Repository", "BaseRepository"]

BaseRepository = TypeVar("BaseRepository", bound="Repository")


class Repository(ABC):
    """Base repository interface.

    All repositories must implement this interface.

    Examples:
        >>> from app.pkg.models.user import StrictUser
        >>> from app.pkg.models.user import (
        ...     CreateUserCommand,
        ...     UpdateUserCommand,
        ...     DeleteUserCommand,
        ...     ReadUserByIdQuery,
        ... )
        >>> class UserRepository(Repository):
        ...     async def create(self, cmd: CreateUserCommand) -> StrictUser:
        ...         ...
        ...
        ...     async def read(self, query: ReadUserByIdQuery) -> StrictUser:
        ...         ...
        ...
        ...     async def read_all(self) -> List[StrictUser]:
        ...         ...
        ...
        ...     async def update(self, cmd: UpdateUserCommand) -> StrictUser:
        ...         ...
        ...
        ...     async def delete(self, cmd: DeleteUserCommand) -> StrictUser:
        ...         ...

    Notes:
        All methods must be asynchronous.

    Warnings:
        #. You must use ``query`` for search model in database and ``cmd`` for create,
           update and delete model in database.
        #. ``query`` and ``cmd`` must be inherited from ``Model`` returning type.
        #. Delete method must return **MARKED** row for delete.
           It is necessary for correct work of the repository layer.
           Repository cant delete row from database.
           It can only mark row as deleted.
        #. All methods must return model contains all fields.
    """

    async def create(self, cmd: Model) -> Model:
        """Create model.

        Args:
            cmd (Model): Specific command for create model. Must be inherited from
                ``Model``.

        Returns:
            Type of the parent model.
        """
        raise NotImplementedError

    async def read(self, query: Model) -> Model:
        """Read model.

        Args:
            query (Model): Specific query for read model. Must be inherited from
                ``Model``.

        Returns:
            Type of the parent model.
        """

        raise NotImplementedError

    async def read_all(self) -> List[Model]:
        """Read all rows."""

        raise NotImplementedError

    async def update(self, cmd: Model) -> Model:
        """Update model.

        Notes: In this method cmd must contain id of the model for update and ALL
        fields for update.

        Returns:
            Type of the parent model.
        """

        raise NotImplementedError

    async def delete(self, cmd: Model) -> Model:
        """Delete model.

        Notes: In this method you should mark row as deleted. You must not delete row
            from database.

        Returns:
            Type of the parent model.
        """

        raise NotImplementedError
