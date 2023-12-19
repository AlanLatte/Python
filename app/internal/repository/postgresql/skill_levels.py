"""Repository for skill levels."""

from typing import List

from app.internal.repository.postgresql.connection import get_connection
from app.internal.repository.postgresql.handlers.collect_response import (
    collect_response,
)
from app.internal.repository.repository import Repository
from app.pkg import models

__all__ = ["SkillLevelRepository"]


class SkillLevelRepository(Repository):
    """Repository for skill levels."""

    @collect_response
    async def create(self, cmd: models.CreateSkillLevelCommand) -> models.SkillLevel:
        q = """
            insert into skill_levels(
                level, description
            ) values (
                %(level)s,
                %(description)s
            )
            returning id, level, description;
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()

    @collect_response
    async def read(self, query: models.ReadSkillLevelQuery) -> models.SkillLevel:
        q = """
            select
                id, level, description
            from skill_levels
            where id = %(id)s;
        """
        async with get_connection() as cur:
            await cur.execute(q, query.to_dict())
            return await cur.fetchone()

    @collect_response
    async def read_all(self) -> List[models.SkillLevel]:
        q = """
            select
                id, level, description
            from skill_levels;
        """
        async with get_connection() as cur:
            await cur.execute(q)
            return await cur.fetchall()

    @collect_response
    async def update(self, cmd: models.UpdateSkillLevelCommand) -> models.SkillLevel:
        q = """
            update skill_levels
            set
                level = %(level)s,
                description = %(description)s
            where id = %(id)s
            returning id, level, description;
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()

    @collect_response
    async def delete(self, cmd: models.DeleteSkillLevelCommand) -> models.SkillLevel:
        q = """
            delete from skill_levels
            where id = %(id)s
            returning id, level, description;
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()
