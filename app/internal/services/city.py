"""Service for manage cities."""


import typing

from app.internal.repository.postgresql import city
from app.internal.repository.repository import BaseRepository
from app.pkg import models
from app.pkg.models.exceptions.city import CityNotFound, NoCityFoundForCountry
from app.pkg.models.exceptions.repository import EmptyResult, UniqueViolation

__all__ = ["CityService"]


class CityService:
    """Service for manage cities."""

    #: CityRepository: CityRepository repository implementation.
    repository: city.CityRepository

    def __init__(self, city_repository: BaseRepository):
        self.repository = city_repository

    async def create_city(self, cmd: models.CreateCityCommand) -> models.City:
        """Create city.

        Args:
            cmd: CreateCityCommand command.

        Returns:
            City: Created city.
        """
        return await self.repository.create(cmd=cmd)

    async def read_city(self, query: models.ReadCityQuery) -> models.City:
        """Read city.

        Args:
            query: ReadCityQuery query.

        Returns:
            City: Read city.
        """
        try:
            return await self.repository.read(query=query)
        except EmptyResult as e:
            raise CityNotFound from e

    async def read_cities_by_country(
        self,
        query: models.ReadCityByCountryQuery,
    ) -> typing.List[models.City]:
        """Read cities by country.

        Args:
            query: ReadCityByCountryQuery query.

        Returns:
            List[City]: Read cities by country.
        """
        try:
            return await self.repository.read_by_country(query=query)
        except EmptyResult as e:
            raise NoCityFoundForCountry from e

    async def read_all_cities(self) -> typing.List[models.City]:
        """Read all cities.

        Returns:
            List[City]: Read all cities.
        """
        try:
            return await self.repository.read_all()
        except EmptyResult as e:
            raise CityNotFound from e

    async def update_city(self, cmd: models.UpdateCityCommand) -> models.City:
        """Update city.

        Args:
            cmd: UpdateCityCommand command.

        Returns:
            City: Updated city.
        """
        try:
            return await self.repository.update(cmd=cmd)
        except UniqueViolation as e:
            raise e

    async def delete_city(self, cmd: models.DeleteCityCommand) -> models.City:
        """Delete city.

        Args:
            cmd: DeleteCityCommand command.
        """
        return await self.repository.delete(cmd=cmd)
