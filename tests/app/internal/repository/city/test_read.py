import pytest

from app.pkg import models
from app.pkg.models.exceptions.repository import EmptyResult


@pytest.mark.postgresql
async def test_read(country_inserter, city_repository, city_inserter, create_model):
    result, _ = await country_inserter(country_code="RUS")

    city, city_cmd = await city_inserter(country_id=result.id)

    query = await create_model(models.ReadCityQuery, id=city.id)

    cities = await city_repository.read(query=query)

    assert isinstance(cities, models.City)
    assert cities == city_cmd.migrate(model=models.City, extra_fields={"id": city.id})


@pytest.mark.postgresql
async def test_city_not_found(city_repository, create_model):
    query = await create_model(models.ReadCityQuery)

    with pytest.raises(EmptyResult):
        await city_repository.read(query=query)
