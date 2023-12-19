from typing import Type

import pytest

from app.internal.repository.repository import Repository
from app.pkg import models
from app.pkg.models.base import Model


async def __inserter(
    repository: Repository,
    generator,
    cmd_model: Type[Model],
    **kwargs,
) -> tuple[Model, Model]:
    """Insert generic model to database.

    Args:
        repository (Repository): Repository instance.
        generator (Callable[..., Model]): Model generator.
        cmd_model (Type[Model]): Command model.
        **kwargs: Model fields.

    Returns:
        tuple[Model, Model]: Tuple with result of insert and command.
    """

    cmd = generator(**kwargs).migrate(model=cmd_model)

    return await repository.create(cmd=cmd), cmd


@pytest.fixture()
async def country_inserter(country_repository, country_generator):
    """Insert country to database."""

    return lambda **kwargs: __inserter(
        repository=country_repository,
        generator=country_generator,
        cmd_model=models.CreateCountryCommand,
        **kwargs,
    )


@pytest.fixture()
async def city_inserter(city_repository, city_generator):
    """Insert city to database."""

    return lambda **kwargs: __inserter(
        repository=city_repository,
        generator=city_generator,
        cmd_model=models.CreateCityCommand,
        **kwargs,
    )


@pytest.fixture()
async def contact_inserter(contact_repository, contact_generator):
    """Insert contact to database."""

    return lambda **kwargs: __inserter(
        repository=contact_repository,
        generator=contact_generator,
        cmd_model=models.CreateContactsCommand,
        **kwargs,
    )


@pytest.fixture()
async def direction_inserter(direction_repository, direction_generator):
    """Insert direction to database."""

    return lambda **kwargs: __inserter(
        repository=direction_repository,
        generator=direction_generator,
        cmd_model=models.CreateDirectionCommand,
        **kwargs,
    )


@pytest.fixture()
async def skill_inserter(skill_repository, skill_generator):
    """Insert skill to database."""

    return lambda **kwargs: __inserter(
        repository=skill_repository,
        generator=skill_generator,
        cmd_model=models.CreateSkillCommand,
        **kwargs,
    )


@pytest.fixture()
async def skill_level_inserter(skill_level_repository, skill_level_generator):
    """Insert skill level to database."""

    return lambda **kwargs: __inserter(
        repository=skill_level_repository,
        generator=skill_level_generator,
        cmd_model=models.CreateSkillLevelCommand,
        **kwargs,
    )


@pytest.fixture()
async def partner_inserter(partner_repository, partner_generator):
    """Insert partner to database."""

    return lambda **kwargs: __inserter(
        repository=partner_repository,
        generator=partner_generator,
        cmd_model=models.CreatePartnerCommand,
        **kwargs,
    )
