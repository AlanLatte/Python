from typing import List

from app.internal.repository.postgresql.connection import get_connection
from app.internal.repository.postgresql.handlers.collect_response import (
    collect_response,
)
from app.internal.repository.repository import Repository
from app.pkg import models
from app.pkg.models.base import Model

__all__ = ["UserRole"]


class UserRole(Repository):
    @collect_response
    async def create(self, cmd: models.CreateUserRoleCommand) -> models.UserRole:
        q = """
            insert into user_roles(role_name)
                values (%(role_name)s) on conflict do nothing
            returning *;
        """

        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict(show_secrets=True))
            return await cur.fetchone()

    async def read(self, query: Model) -> Model:
        raise NotImplementedError

    async def read_all(self) -> List[Model]:
        raise NotImplementedError

    async def update(self, cmd: Model) -> Model:
        raise NotImplementedError

    async def delete(self, cmd: Model) -> Model:
        raise NotImplementedError
