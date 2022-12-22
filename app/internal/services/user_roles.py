from app.internal.repository.postgresql import user_roles
from app.internal.repository.repository import BaseRepository
from app.pkg import models

__all__ = ["UserRoleService"]


class UserRoleService:
    #: user_roles.UserRoleRepository: UserRoleRepository repository implementation.
    repository: user_roles.UserRoleRepository

    def __init__(self, user_role_repository: BaseRepository):
        self.repository = user_role_repository

    async def create_all_user_roles(self) -> None:
        for role in models.UserRole:
            await self.repository.create(
                cmd=models.CreateUserRoleCommand(role_name=role),
            )
