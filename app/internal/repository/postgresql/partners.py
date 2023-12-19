"""Repository for partners."""
from typing import List

from app.internal.repository.postgresql.connection import get_connection
from app.internal.repository.postgresql.handlers.collect_response import (
    collect_response,
)
from app.internal.repository.repository import Repository
from app.pkg import models

__all__ = ["PartnerRepository"]


class PartnerRepository(Repository):
    """Repository for partners."""

    @collect_response
    async def create(self, cmd: models.CreatePartnerCommand) -> models.Partner:
        q = """
            insert into partners(
                name,
                token
            ) values (
                %(name)s,
                %(token)s
            )
            returning id, name, token
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()

    @collect_response
    async def read(self, query: models.ReadPartnerQuery) -> models.Partner:
        q = """
            select
                id, name, token
            from partners
            where id = %(id)s
        """
        async with get_connection() as cur:
            await cur.execute(q, query.to_dict())
            return await cur.fetchone()

    @collect_response
    async def read_by_token(
        self,
        query: models.ReadPartnerByTokenQuery,
    ) -> models.Partner:
        q = """
            select
                id, name, token
            from partners
            where token = %(token)s
        """
        async with get_connection() as cur:
            await cur.execute(q, query.to_dict())
            return await cur.fetchone()

    @collect_response
    async def read_all(self) -> List[models.Partner]:
        q = """
            select
                id, name, token
            from partners
        """
        async with get_connection() as cur:
            await cur.execute(q)
            return await cur.fetchall()

    @collect_response
    async def update(self, cmd: models.UpdatePartnerCommand) -> models.Partner:
        q = """
            update partners
            set
                name = %(name)s,
                token = %(token)s
            where id = %(id)s
            returning id, name, token
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()

    @collect_response
    async def delete(self, cmd: models.DeletePartnerCommand) -> models.Partner:
        q = """
            delete from partners
            where id = %(id)s
            returning id, name, token
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()
