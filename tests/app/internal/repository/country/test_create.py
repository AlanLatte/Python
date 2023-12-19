import asyncio

import pytest
from pydantic.error_wrappers import ValidationError

from app.internal.repository.postgresql.country import CountryRepository
from app.pkg import models
from app.pkg.models.exceptions.country import (
    CountryCodeAlreadyExists,
    CountryNameAlreadyExists,
)


@pytest.mark.postgresql
@pytest.mark.parametrize(
    "country_code",
    [
        "RUS",
        "USA",
    ],
)
async def test_correct(
    country_repository: CountryRepository, create_model, country_code,
):
    cmd = await create_model(models.CreateCountryCommand, code=country_code)

    result = await country_repository.create(cmd=cmd)
    assert result == cmd.migrate(model=models.Country, extra_fields={"id": result.id})


@pytest.mark.postgresql
@pytest.mark.parametrize(
    "country_name",
    [
        "Russia",
        "USA",
    ],
)
async def test_unique_country_name(
    country_repository: CountryRepository, country_name: str, create_model,
):
    commands = []
    for _ in range(2):
        cmd = await create_model(models.CreateCountryCommand, name=country_name)
        commands.append(asyncio.create_task(country_repository.create(cmd=cmd)))

    with pytest.raises(CountryNameAlreadyExists):
        await asyncio.gather(*commands)


@pytest.mark.parametrize(
    "country_name",
    [
        "Russia",
        " Russia",
        "Russia ",
        " Russia ",
        "Russia  ",
        "  Russia",
    ],
)
async def test_strip_whitespace_country_name(country_name: str, create_model):
    cmd = await create_model(models.CreateCountryCommand, name=country_name)
    assert cmd.name == country_name.strip()


@pytest.mark.parametrize(
    "country_code",
    [
        "RUS",
        " RUS",
        "RUS ",
        " RUS ",
        "RUS  ",
        "  RUS",
    ],
)
async def test_strip_whitespace_country_code(country_code: str, create_model):
    cmd = await create_model(models.CreateCountryCommand, code=country_code)
    assert cmd.code == country_code.strip()


@pytest.mark.postgresql
@pytest.mark.parametrize(
    "country_code",
    [
        "RUS",
        "USA",
        "CAN",
        "CHN",
        "JPN",
        "DEU",
        "FRA",
        "ITA",
    ],
)
async def test_country_code_already_exists(
    country_repository: CountryRepository, country_code: str, create_model,
):
    commands = []
    for _ in range(2):
        cmd = await create_model(models.CreateCountryCommand, code=country_code)
        commands.append(asyncio.create_task(country_repository.create(cmd=cmd)))

    with pytest.raises(CountryCodeAlreadyExists):
        await asyncio.gather(*commands)


@pytest.mark.parametrize(
    "country_code",
    [
        "RU",
        "US",
        "CA",
        "CN",
        "JP",
        "DE",
        "FR",
        "IT",
        "AF",
        "AL",
        "DZ",
        "AS",
    ],
)
async def test_country_code_length(create_model, country_code: str):
    with pytest.raises(ValidationError):
        await create_model(models.CreateCountryCommand, code=country_code)
