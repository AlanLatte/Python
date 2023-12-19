"""Module for testing read method of country repository."""


import pytest

from app.internal.repository.postgresql.country import CountryRepository
from app.pkg import models
from app.pkg.models.exceptions.repository import EmptyResult


@pytest.mark.postgresql
@pytest.mark.parametrize(
    "country_code",
    [
        "RUS",
        "USA",
    ],
)
async def test_correct(country_code, country_inserter):
    result, cmd = await country_inserter(country_code=country_code)

    assert result == cmd.migrate(model=models.Country, extra_fields={"id": result.id})


@pytest.mark.postgresql
async def test_country_not_found(
    country_repository: CountryRepository,
    country_inserter,
    create_model,
):
    result, _ = await country_inserter()

    query = await create_model(models.ReadCountryQuery, id=result.id + 1)

    with pytest.raises(EmptyResult):
        await country_repository.read(query=query)
