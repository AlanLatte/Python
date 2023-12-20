"""Fixtures for services."""

import pytest

from app.internal.repository.postgresql import CityRepository, CountryRepository
from app.internal.services import CountryService
from app.internal.services.city import CityService


@pytest.fixture()
async def city_service(city_repository: CityRepository) -> CityService:
    return CityService(city_repository=city_repository)


@pytest.fixture()
async def country_service(country_repository: CountryRepository) -> CountryService:
    return CountryService(country_repository=country_repository)
