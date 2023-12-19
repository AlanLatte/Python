import pytest

from app.pkg import models
from app.pkg.models.exceptions.repository import EmptyResult


@pytest.mark.postgresql
@pytest.mark.slow
async def test_delete(city_repository, country_inserter, city_inserter, clean_postgres):
    _ = clean_postgres

    result, _ = await country_inserter(country_code="RUS")

    city, city_cmd = await city_inserter(country_id=result.id)

    cmd = city.migrate(
        models.DeleteCityCommand,
        extra_fields={"id": city.id},
    )

    await city_repository.delete(cmd=cmd)

    with pytest.raises(EmptyResult):
        await city_repository.read(
            query=city.migrate(models.ReadCityQuery, extra_fields={"id": city.id}),
        )


@pytest.mark.postgresql
async def test_city_not_found(city_repository, create_model):
    cmd = await create_model(models.DeleteCityCommand)

    with pytest.raises(EmptyResult):
        await city_repository.delete(cmd=cmd)
