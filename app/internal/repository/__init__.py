"""Module ``Repository`` must contain **CRUD** methods.

Note:
    The repository must contain a minimum set of instructions for interacting with the
    target database.

Examples:
    Let's say we have a User repository. For its correct operation, 5 implemented
    methods are sufficient.::

        >>> from app.internal.repository.repository import Repository
        >>> from typing import List
        >>> from app.pkg.models.user import (
        ...     CreateUserCommand,
        ...     DeleteUserCommand,
        ...     UpdateUserCommand,
        ...     ReadUserByUserNameQuery,
        ...     User,
        ... )
        ...
        >>> class UserRepository(Repository):
        ...     async def create(self, cmd: CreateUserCommand) -> User:
        ...         ...
        ...
        ...     async def read(self, query: ReadUserByUserNameQuery) -> User:
        ...         ...
        ...
        ...     async def read_all(self) -> List[User]:
        ...         ...
        ...
        ...     async def update(self, cmd: UpdateUserCommand) -> User:
        ...         ...
        ...
        ...     async def delete(self, cmd: DeleteUserCommand) -> User:
        ...         ...


    If, for example, you need to update the password, you will need to use 2 methods
    in the implemented service method.::

        >>> from app.pkg.models.user import ChangeUserPasswordCommand, UpdateUserCommand
        >>> from app.internal.repository.postgresql.user import UserRepository
        >>> class UserService:
        ...    repository: UserRepository
        ...
        ...    async def change_password(self, cmd: ChangeUserPasswordCommand):
        ...        user = await self.repository.read(cmd=cmd)
        ...        user.password = cmd.new_password
        ...        user.migrate(ChangeUserPasswordCommand)
        ...        return self.repository.update(cmd=cmd.migrate(UpdateUserCommand))
"""

from dependency_injector import containers, providers

from . import postgresql
from .repository import BaseRepository

__all__ = ["Repositories"]


class Repositories(containers.DeclarativeContainer):
    postgres = providers.Container(postgresql.Repositories)
