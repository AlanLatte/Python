"""Module for testing city repository update method."""


import asyncio

import pytest

from app.pkg import models
from app.pkg.models.exceptions.city import CityNameAlreadyExists, DuplicateCityCode
from app.pkg.models.exceptions.repository import EmptyResult


@pytest.mark.postgresql
async def test_update(city_repository, city_inserter, country_inserter):
    country, _ = await country_inserter(country_code="RUS")
    city, _ = await city_inserter(country_id=country.id)

    cmd = city.migrate(
        models.UpdateCityCommand,
        extra_fields={"name": "Moscow", "code": "MSK"},
    )

    await city_repository.update(cmd=cmd)

    result = await city_repository.read(
        query=city.migrate(models.ReadCityQuery, extra_fields={"id": city.id}),
    )

    assert result == cmd.migrate(model=models.City, extra_fields={"id": city.id})


@pytest.mark.postgresql
async def test_city_not_found(
    city_repository,
    create_model,
    country_inserter,
    city_inserter,
):
    result, _ = await country_inserter()
    city, _ = await city_inserter(country_id=result.id)
    cmd = await create_model(models.UpdateCityCommand, id=city.id + 1)

    with pytest.raises(EmptyResult):
        await city_repository.update(cmd=cmd)


@pytest.mark.postgresql
async def test_duplicate_city_code(
    city_repository,
    create_model,
    country_inserter,
    clean_postgres,
):
    _ = clean_postgres

    result, _ = await country_inserter()

    cmd_1 = await create_model(
        models.CreateCityCommand,
        country_id=result.id,
        code="MSK",
        name="Ufa",
    )
    cmd_2 = await create_model(
        models.CreateCityCommand,
        country_id=result.id,
        code="MSK",
        name="Moscow",
    )

    tasks = [
        asyncio.create_task(city_repository.create(cmd=cmd_1)),
        asyncio.create_task(city_repository.create(cmd=cmd_2)),
    ]

    with pytest.raises(DuplicateCityCode):
        await asyncio.gather(*tasks)


@pytest.mark.postgresql
async def test_duplicate_city_name(
    city_repository,
    create_model,
    country_inserter,
    clean_postgres,
):
    _ = clean_postgres

    result, _ = await country_inserter()

    cmd_1 = await create_model(
        models.CreateCityCommand,
        country_id=result.id,
        code="UFA",
        name="Moscow",
    )
    cmd_2 = await create_model(
        models.CreateCityCommand,
        country_id=result.id,
        code="MSK",
        name="Moscow",
    )

    tasks = [
        asyncio.create_task(city_repository.create(cmd=cmd_1)),
        asyncio.create_task(city_repository.create(cmd=cmd_2)),
    ]

    with pytest.raises(CityNameAlreadyExists):
        await asyncio.gather(*tasks)
