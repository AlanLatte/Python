"""Repositories should be dumb, while services, on the contrary, should be
smart. That's why :class:`.Repository` must contain a minimum set of.

**C.R.U.D.** methods.

- **C** - Create
- **R** - Read
- **U** - Update
- **D** - Delete

Note:
    The repository must contain a minimum set of instructions for interacting with the
    target database.

Examples:
    Let's say we have a StrictUser repository. For its correct operation,
    five implemented methods are sufficient.::

        >>> from app.internal.repository.repository import Repository
        >>> from typing import List
        >>> from app.pkg.models.user import (
        ...     CreateUserCommand,
        ...     DeleteUserCommand,
        ...     UpdateUserCommand,
        ...     ReadUserByUserNameQuery,
        ...     StrictUser,
        ... )
        ...
        >>> class UserRepository(Repository):
        ...     async def create(self, cmd: CreateUserCommand) -> StrictUser:
        ...         ...
        ...
        ...     async def read(self, query: ReadUserByUserNameQuery) -> StrictUser:
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


    If, for example, you need to update the password, you will need to use two methods
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

from app.internal.repository import postgresql

__all__ = ["Repositories"]


class Repositories(containers.DeclarativeContainer):
    """Container for repositories.

    Attributes:
        postgres (providers.Container): Container for postgresql repositories.

    Notes:
        If you want to add a new repository,
        you **must** add it to this container.
    """

    postgres = providers.Container(postgresql.Repositories)
