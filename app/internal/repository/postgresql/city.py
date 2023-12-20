"""Repository for cities."""

from typing import List

from app.internal.repository.postgresql.connection import get_connection
from app.internal.repository.postgresql.handlers.collect_response import (
    collect_response,
)
from app.internal.repository.repository import Repository
from app.pkg import models

__all__ = ["CityRepository"]


class CityRepository(Repository):
    """City repository implementation."""

    @collect_response
    async def create(self, cmd: models.CreateCityCommand) -> models.City:
        q = """
            insert into cities(
                name, code, country_id
            ) values (
                %(name)s, %(code)s, %(country_id)s
            )
            returning id, name, code, country_id
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()

    @collect_response
    async def read(self, query: models.ReadCityQuery) -> models.City:
        q = """
            select
                id, name, code, country_id
            from cities
            where id = %(id)s
        """
        async with get_connection() as cur:
            await cur.execute(q, query.to_dict())
            return await cur.fetchone()

    @collect_response
    async def read_by_country(
        self,
        query: models.ReadCityByCountryQuery,
    ) -> List[models.City]:
        q = """
            select
                id, name, code, country_id
            from cities
            where country_id = %(country_id)s
        """
        async with get_connection() as cur:
            await cur.execute(q, query.to_dict())
            return await cur.fetchall()

    @collect_response
    async def read_all(self) -> List[models.City]:
        q = """
            select
                id, name, code, country_id
            from cities
        """
        async with get_connection() as cur:
            await cur.execute(q)
            return await cur.fetchall()

    @collect_response
    async def update(self, cmd: models.UpdateCityCommand) -> models.City:
        q = """
            update cities
            set
                name = %(name)s,
                code = %(code)s,
                country_id = %(country_id)s
            where id = %(id)s
            returning id, name, code, country_id
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()

    @collect_response
    async def delete(self, cmd: models.DeleteCityCommand) -> models.City:
        q = """
            delete from cities
            where id = %(id)s
            returning id, name, code, country_id
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()
