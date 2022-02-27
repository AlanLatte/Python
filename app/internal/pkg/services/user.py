"""User service."""
from typing import List

from app.internal.pkg.repository.postgresql import user
from app.internal.pkg.repository.repository import BaseRepository
from app.pkg import models
from app.pkg.models.exceptions.repository import UniqueViolation
from app.pkg.models.exceptions.user import UserAlreadyExist


class User:
    repository: user.User

    def __init__(self, user_repository: BaseRepository):
        self.repository = user_repository

    async def create_user(self, cmd: models.CreateUserCommand) -> models.User:
        """Function for create user.
        Args:
            cmd: `CreateUserCommand`.

        Returns:
            `User` model.

        Raises:
            UserAlreadyExist: when email of user already taken in database.
        """
        try:
            return await self.repository.create(cmd=cmd)
        except UniqueViolation:
            raise UserAlreadyExist

    async def read_all_users(self) -> List[models.User]:
        return await self.repository.read_all()

    async def read_specific_user_by_email(
        self, query: models.ReadUserByEmailQuery
    ) -> models.User:
        return await self.repository.read_by_email(query=query)

    async def read_specific_user_by_id(
        self, query: models.ReadUserByIdQuery
    ) -> models.User:
        return await self.repository.read(query=query)

    async def change_password(
        self, cmd: models.ChangeUserPasswordCommand
    ) -> models.User:
        ...

    async def delete_specific_user(self, cmd: models.DeleteUserCommand) -> models.User:
        return await self.repository.delete(cmd=cmd)
