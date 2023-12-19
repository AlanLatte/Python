"""Repository for countries."""

from typing import List

from app.internal.repository.postgresql.connection import get_connection
from app.internal.repository.postgresql.handlers.collect_response import (
    collect_response,
)
from app.internal.repository.repository import Repository
from app.pkg import models

__all__ = ["CountryRepository"]


class CountryRepository(Repository):
    """Country repository implementation."""

    @collect_response
    async def create(self, cmd: models.CreateCountryCommand) -> models.Country:
        q = """
            insert into countries(
                name, code
            ) values (
                %(name)s, %(code)s
            )
            returning id, name, code
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()

    @collect_response
    async def read(self, query: models.ReadCountryQuery) -> models.Country:
        q = """
            select
                id, name, code
            from countries
            where id = %(id)s
        """
        async with get_connection() as cur:
            await cur.execute(q, query.to_dict())
            return await cur.fetchone()

    @collect_response
    async def read_all(self) -> List[models.Country]:
        q = """
            select
                id, name, code
            from countries
        """
        async with get_connection() as cur:
            await cur.execute(q)
            return await cur.fetchall()

    @collect_response
    async def update(self, cmd: models.UpdateCountryCommand) -> models.Country:
        q = """
            update countries
            set
                name = %(name)s,
                code = %(code)s
            where id = %(id)s
            returning id, name, code
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()

    @collect_response
    async def delete(self, cmd: models.DeleteCountryCommand) -> models.Country:
        q = """
            delete from countries
            where id = %(id)s
            returning id, name, code
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()
