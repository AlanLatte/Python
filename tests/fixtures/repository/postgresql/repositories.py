"""All fixtures for postgresql repositories."""

import pytest

from app.internal.repository.postgresql import (
    CityRepository,
    ContactsRepository,
    CountryRepository,
    DirectionRepository,
    PartnerRepository,
    SkillLevelRepository,
    SkillRepository,
)


@pytest.fixture()
async def city_repository() -> CityRepository:
    return CityRepository()


@pytest.fixture()
async def country_repository() -> CountryRepository:
    return CountryRepository()


@pytest.fixture()
async def contact_repository() -> ContactsRepository:
    return ContactsRepository()


@pytest.fixture()
async def direction_repository() -> DirectionRepository:
    return DirectionRepository()


@pytest.fixture()
async def skill_repository() -> SkillRepository:
    return SkillRepository()


@pytest.fixture()
async def skill_level_repository() -> SkillLevelRepository:
    return SkillLevelRepository()


@pytest.fixture()
async def partner_repository() -> PartnerRepository:
    return PartnerRepository()
