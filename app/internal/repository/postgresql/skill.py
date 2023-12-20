"""Repository for skill model."""

from typing import List

from app.internal.repository.postgresql.connection import get_connection
from app.internal.repository.postgresql.handlers.collect_response import (
    collect_response,
)
from app.internal.repository.repository import Repository
from app.pkg import models

__all__ = ["SkillRepository"]


class SkillRepository(Repository):
    """Skill repository implementation."""

    @collect_response
    async def create(self, cmd: models.CreateSkillCommand) -> models.Skill:
        q = """
            insert into skills(
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
    async def read(self, query: models.ReadSkillQuery) -> models.Skill:
        q = """
            select
                id, name
            from skills
            where id = %(id)s
        """
        async with get_connection() as cur:
            await cur.execute(q, query.to_dict())
            return await cur.fetchone()

    @collect_response
    async def batch_read_all(
        self,
        query: models.ReadAllSkillByIdQuery,
    ) -> List[models.Skill]:
        q = """
                select
                    id, name
                from skills
                where id = ANY(%(ids)s)
            """
        async with get_connection() as cur:
            await cur.execute(q, query.to_dict())
            return await cur.fetchall()

    @collect_response
    async def read_all(self) -> List[models.Skill]:
        q = """
            select
                id, name
            from skills
        """
        async with get_connection() as cur:
            await cur.execute(q)
            return await cur.fetchall()

    @collect_response
    async def update(self, cmd: models.UpdateSkillCommand) -> models.Skill:
        q = """
            update skills
            set
                name = %(name)s
            where id = %(id)s
            returning id, name
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()

    @collect_response
    async def delete(self, cmd: models.DeleteSkillCommand) -> models.Skill:
        q = """
            delete from skills
            where id = %(id)s
            returning id, name
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()
