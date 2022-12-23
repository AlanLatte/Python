import typing

from app.internal.repository.postgresql import user_roles
from app.internal.repository.repository import BaseRepository
from app.pkg import models
from app.pkg.models.base import BaseAPIException
from app.pkg.models.exceptions.repository import DriverError, UniqueViolation

__all__ = ["UserRoleService"]


class UserRoleService:
    #: user_roles.UserRoleRepository: UserRoleRepository repository implementation.
    repository: user_roles.UserRoleRepository

    def __init__(self, user_role_repository: BaseRepository):
        self.repository = user_role_repository

    async def create_all_user_roles(
        self,
    ) -> typing.AsyncIterable[typing.Optional[BaseAPIException]]:
        for role in models.UserRole:
            try:
                await self.repository.create(
                    cmd=models.CreateUserRoleCommand(role_name=role),
                )
            except DriverError as e:
                yield e
            except UniqueViolation:
                continue
