"""Module for testing update method of country repository."""

import uuid

import pytest

from app.internal.repository.postgresql import CountryRepository
from app.pkg import models
from app.pkg.models.exceptions.country import (
    CountryCodeAlreadyExists,
    CountryNameAlreadyExists,
)
from app.pkg.models.exceptions.repository import EmptyResult


@pytest.mark.postgresql
async def test_correct(country_repository: CountryRepository, country_inserter):
    result, _ = await country_inserter()
    cmd = result.migrate(model=models.UpdateCountryCommand)

    after_update = await country_repository.update(cmd=cmd)
    assert after_update == cmd.migrate(
        model=models.Country,
        extra_fields={"id": result.id},
    )


@pytest.mark.postgresql
async def test_country_not_found(
    country_repository: CountryRepository,
    country_inserter,
    create_model,
):
    result, _ = await country_inserter()
    cmd = await create_model(models.UpdateCountryCommand, id=result.id + 1)

    with pytest.raises(EmptyResult):
        await country_repository.update(cmd=cmd)


@pytest.mark.postgresql
async def test_unique_country_name(
    country_repository: CountryRepository,
    country_inserter,
):
    old_result, _ = await country_inserter()

    result, _ = await country_inserter()
    cmd = result.migrate(
        model=models.UpdateCountryCommand,
        extra_fields={"name": old_result.name},
    )

    with pytest.raises(CountryNameAlreadyExists):
        await country_repository.update(cmd=cmd)


@pytest.mark.postgresql
async def test_unique_country_code(
    country_repository: CountryRepository,
    country_inserter,
):
    old_result, _ = await country_inserter()
    result, _ = await country_inserter()
    cmd = result.migrate(
        model=models.UpdateCountryCommand,
        extra_fields={"code": old_result.code, "name": uuid.uuid4().hex},
    )

    with pytest.raises(CountryCodeAlreadyExists):
        await country_repository.update(cmd=cmd)


@pytest.mark.postgresql
@pytest.mark.repeat(5)
async def test_unique_country_code_and_name(
    country_repository: CountryRepository,
    country_inserter,
):
    old_result, _ = await country_inserter()
    new_result, _ = await country_inserter()
    cmd = old_result.migrate(
        model=models.UpdateCountryCommand,
        extra_fields={"id": new_result.id},
    )

    with pytest.raises(CountryNameAlreadyExists):
        await country_repository.update(cmd=cmd)


@pytest.mark.postgresql
@pytest.mark.parametrize(
    "country_name",
    [
        "Russia",
        "Russia ",
        " Russia",
        " Russia ",
        "Russia  ",
        "  Russia",
    ],
)
async def test_strip_whitespace_country_name(country_name: str, create_model):
    cmd = await create_model(models.UpdateCountryCommand, name=country_name)

    assert cmd.name == country_name.strip()
