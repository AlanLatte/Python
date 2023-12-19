"""Repository for contacts."""
from typing import List

from app.internal.repository.postgresql.connection import get_connection
from app.internal.repository.postgresql.handlers.collect_response import (
    collect_response,
)
from app.internal.repository.repository import Repository
from app.pkg import models

__all__ = ["DirectionRepository"]


class DirectionRepository(Repository):
    """Direction repository implementation."""

    @collect_response
    async def create(self, cmd: models.CreateDirectionCommand) -> models.Direction:
        q = """
            insert into directions(
                name
            ) values (
                %(name)s
            )
            returning id, name
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()

    @collect_response
    async def read(self, query: models.ReadDirectionQuery) -> models.Direction:
        q = """
            select
                id, name
            from directions
            where id = %(id)s
        """
        async with get_connection() as cur:
            await cur.execute(q, query.to_dict())
            return await cur.fetchone()

    @collect_response
    async def batch_read_all(
        self,
        query: models.ReadAllDirectionByIdQuery,
    ) -> List[models.Direction]:
        q = """
                select
                    id, name
                from directions
                where id = ANY(%(ids)s)
            """
        async with get_connection() as cur:
            await cur.execute(q, query.to_dict())
            return await cur.fetchall()

    @collect_response
    async def read_all(self) -> List[models.Direction]:
        q = """
            select
                id, name
            from directions
        """
        async with get_connection() as cur:
            await cur.execute(q)
            return await cur.fetchall()

    @collect_response
    async def update(self, cmd: models.UpdateDirectionCommand) -> models.Direction:
        q = """
            update directions
            set
                name = %(name)s
            where id = %(id)s
            returning id, name
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()

    @collect_response
    async def delete(self, cmd: models.DeleteDirectionCommand) -> models.Direction:
        q = """
            delete from directions
            where id = %(id)s
            returning id, name
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()
