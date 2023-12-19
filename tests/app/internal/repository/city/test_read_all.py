"""Model City read_all method tests."""

import pytest

from app.pkg import models
from app.pkg.models.exceptions.repository import EmptyResult


@pytest.mark.postgresql
@pytest.mark.slow
async def test_read_all(
    city_repository,
    city_inserter,
    country_inserter,
    clean_postgres,
):
    _ = clean_postgres

    result, _ = await country_inserter(country_code="RUS")
    city, city_cmd = await city_inserter(country_id=result.id)

    cities = await city_repository.read_all()

    assert isinstance(cities, list)
    assert len(cities) == 1

    for response_city in cities:
        assert isinstance(response_city, models.City)
        assert response_city == city_cmd.migrate(
            model=models.City,
            extra_fields={"id": city.id},
        )


@pytest.mark.postgresql
@pytest.mark.slow
async def test_read_all_empty(city_repository, clean_postgres):
    _ = clean_postgres

    with pytest.raises(EmptyResult):
        await city_repository.read_all()
