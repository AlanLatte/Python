"""User service."""
import typing
from typing import List

from app.internal.pkg.password import password
from app.internal.repository.postgresql import UserRepository
from app.internal.repository.repository import BaseRepository
from app.pkg import models
from app.pkg.models.exceptions.repository import UniqueViolation
from app.pkg.models.exceptions.user import IncorrectOldPassword, UserAlreadyExist

__all__ = ["UserService"]


class UserService:
    repository: UserRepository

    def __init__(self, user_repository: typing.Type[BaseRepository]):
        self.repository = user_repository

    async def create_user(self, cmd: models.CreateUserCommand) -> models.User:
        """Function for create user. User password will be encrypted.

        Args:
            cmd: `CreateUserCommand`.

        Raises:
            UserAlreadyExist: when username of user already taken in repository.

        Returns: `User` model.
        """

        try:
            cmd.password.crypt_password()
            return await self.repository.create(cmd=cmd)
        except UniqueViolation:
            raise UserAlreadyExist

    async def read_all_users(self) -> List[models.User]:
        """Read all users from repository."""
        return await self.repository.read_all()

    async def read_specific_user_by_username(
        self,
        query: models.ReadUserByUserNameQuery,
    ) -> models.User:
        """Read specific user from repository by username.

        Args:
            query: `ReadUserByUserNameQuery`.

        Returns: `User` model.
        """

        return await self.repository.read_by_username(query=query)

    async def read_specific_user_by_id(
        self,
        query: models.ReadUserByIdQuery,
    ) -> models.User:
        """Read specific user from repository by user id.

        Args:
            query: `ReadUserByIdQuery`.

        Returns: `User` model.
        """

        return await self.repository.read(query=query)

    async def change_password(
        self,
        cmd: models.ChangeUserPasswordCommand,
    ) -> models.User:

        """Change password for specific user. `id` is `fk` for match user in
        database.

        Args:
            cmd: `ChangeUserPasswordCommand`.

        Raises:
            IncorrectOldPassword: when the transmitted password does not match the one
                in the database

        Returns: `User` model.
        """

        user = await self.repository.read(query=models.ReadUserByIdQuery(id=cmd.id))

        if not password.check_password(cmd.old_password, user.password):
            raise IncorrectOldPassword

        user.password = cmd.new_password
        return await self.repository.update(cmd=user.migrate(models.UpdateUserCommand))

    async def delete_specific_user(self, cmd: models.DeleteUserCommand) -> models.User:
        """Delete specific user by user id.

        Args:
             cmd: `DeleteUserCommand`.

        Returns: `User` model.
        """

        return await self.repository.delete(cmd=cmd)
