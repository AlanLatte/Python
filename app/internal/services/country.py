"""Models for country object."""

import typing

from app.internal.repository.postgresql import country
from app.internal.repository.repository import BaseRepository
from app.pkg import models
from app.pkg.models.exceptions.country import CountryNameAlreadyExists, CountryNotFound
from app.pkg.models.exceptions.repository import EmptyResult, UniqueViolation

__all__ = ["CountryService"]


class CountryService:
    """Service for manage countries."""

    #: CountryRepository: CountryRepository repository implementation.
    repository: country.CountryRepository

    def __init__(self, country_repository: BaseRepository):
        self.repository = country_repository

    async def create_country(self, cmd: models.CreateCountryCommand) -> models.Country:
        """Create country.

        Args:
            cmd: CreateCountryCommand command.

        Returns:
            Country: Created country.
        """
        try:
            return await self.repository.create(cmd=cmd)
        except UniqueViolation as e:
            raise CountryNameAlreadyExists from e

    async def read_country(self, query: models.ReadCountryQuery) -> models.Country:
        """Read country.

        Args:
            query: ReadCountryQuery query.

        Returns:
            Country: Read country.
        """
        return await self.repository.read(query=query)

    async def read_all_countries(self) -> typing.List[models.Country]:
        """Read all countries.

        Returns:
            List[Country]: Read all countries.
        """
        return await self.repository.read_all()

    async def update_country(self, cmd: models.UpdateCountryCommand) -> models.Country:
        """Update country.

        Args:
            cmd: UpdateCountryCommand command.

        Returns:
            Country: Updated country.
        """
        try:
            return await self.repository.update(cmd=cmd)
        except EmptyResult as e:
            raise CountryNotFound from e

    async def delete_country(self, cmd: models.DeleteCountryCommand) -> models.Country:
        """Delete country.

        Args:
            cmd: DeleteCountryCommand command.
        """
        return await self.repository.delete(cmd=cmd)
