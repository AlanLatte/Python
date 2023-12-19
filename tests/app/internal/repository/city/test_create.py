import asyncio

import pytest
from pydantic.error_wrappers import ValidationError

from app.internal.repository.postgresql.city import CityRepository
from app.pkg import models
from app.pkg.models.exceptions.city import CityNameAlreadyExists, DuplicateCityCode
from app.pkg.models.exceptions.country import CountryNotFound


@pytest.mark.postgresql
async def test_correct(city_repository: CityRepository, create_model, country_inserter):
    result, _ = await country_inserter()
    cmd = await create_model(models.CreateCityCommand, country_id=result.id)
    city = await city_repository.create(cmd=cmd)

    assert isinstance(city, models.City)
    assert city == cmd.migrate(model=models.City, extra_fields={"id": city.id})


@pytest.mark.postgresql
async def test_country_not_found(city_repository: CityRepository, create_model):
    cmd = await create_model(models.CreateCityCommand)
    with pytest.raises(CountryNotFound):
        await city_repository.create(cmd=cmd)


@pytest.mark.postgresql
async def test_duplicate_city_code(
    city_repository: CityRepository, create_model, country_inserter,
):
    result, _ = await country_inserter()
    cmd_1 = await create_model(
        models.CreateCityCommand, country_id=result.id, code="MSK", name="Ufa",
    )
    cmd_2 = await create_model(
        models.CreateCityCommand, country_id=result.id, code="MSK", name="Moscow",
    )
    tasks = [
        asyncio.create_task(city_repository.create(cmd=cmd_1)),
        asyncio.create_task(city_repository.create(cmd=cmd_2)),
    ]

    with pytest.raises(DuplicateCityCode):
        await asyncio.gather(*tasks)


@pytest.mark.postgresql
async def test_duplicate_city_name(
    city_repository: CityRepository, create_model, country_inserter,
):
    result, cmd = await country_inserter()
    cmd_1 = await create_model(
        models.CreateCityCommand, country_id=result.id, code="UFA", name="Moscow",
    )
    cmd_2 = await create_model(
        models.CreateCityCommand, country_id=result.id, code="MSK", name="Moscow",
    )

    tasks = [
        asyncio.create_task(city_repository.create(cmd=cmd_1)),
        asyncio.create_task(city_repository.create(cmd=cmd_2)),
    ]

    with pytest.raises(CityNameAlreadyExists):
        await asyncio.gather(*tasks)


@pytest.mark.parametrize(
    "code",
    [
        "MS",
        "MO",
        "SP",
        "M",
        "SS",
        "S",
        "SO",
    ],
)
async def test_code_length_equal_3(create_model, code: str):
    with pytest.raises(ValidationError):
        await create_model(
            models.CreateCityCommand, code=code, name="Moscow", country_id=1,
        )
