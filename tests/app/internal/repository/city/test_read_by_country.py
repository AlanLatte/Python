import pytest

from app.pkg import models
from app.pkg.models.exceptions.repository import EmptyResult


@pytest.mark.postgresql
async def test_read_by_country(country_inserter, city_repository, city_inserter):
    result, _ = await country_inserter(country_code="RUS")

    city, city_cmd = await city_inserter(country_id=result.id)

    query = result.migrate(
        model=models.ReadCityByCountryQuery, extra_fields={"country_id": result.id},
    )

    cities = await city_repository.read_by_country(query=query)

    assert isinstance(cities, list)
    assert len(cities) == 1

    for __city in cities:
        assert isinstance(__city, models.City)
        assert __city == city_cmd.migrate(
            model=models.City, extra_fields={"id": city.id},
        )


@pytest.mark.postgresql
async def test_read_by_country_empty(country_inserter, city_repository):
    result, _ = await country_inserter(country_code="RUS")

    query = result.migrate(
        model=models.ReadCityByCountryQuery, extra_fields={"country_id": result.id},
    )

    with pytest.raises(EmptyResult):
        await city_repository.read_by_country(query=query)


@pytest.mark.postgresql
async def test_county_not_found(city_repository, create_model):
    query = await create_model(models.ReadCityByCountryQuery)

    with pytest.raises(EmptyResult):
        await city_repository.read_by_country(query=query)
