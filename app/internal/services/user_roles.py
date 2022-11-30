from app.internal.repository.postgresql import user_roles
from app.internal.repository.repository import BaseRepository
from app.pkg import models

__all__ = ["UserRole"]


class UserRole:
    #: user_roles.UserRole: UserRole repository implementation.
    repository: user_roles.UserRole

    def __init__(self, repository: BaseRepository):
        self.repository = repository

    async def create_all_user_roles(self) -> None:
        for role in models.UserRole:
            await self.repository.create(
                cmd=models.CreateUserRoleCommand(role_name=role),
            )
