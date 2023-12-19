"""Module for testing delete method in country repository."""


import pytest

from app.internal.repository.postgresql import CountryRepository
from app.pkg import models
from app.pkg.models.exceptions.repository import EmptyResult


@pytest.mark.postgresql
async def test_correct(country_repository: CountryRepository, country_inserter):
    result, _ = await country_inserter()
    cmd = result.migrate(model=models.DeleteCityCommand)

    await country_repository.delete(cmd=cmd)

    with pytest.raises(EmptyResult):
        await country_repository.read(query=models.ReadCountryQuery(id=result.id))


@pytest.mark.postgresql
async def test_country_not_found(
    country_repository: CountryRepository,
    country_inserter,
    create_model,
):
    result, _ = await country_inserter()
    cmd = await create_model(models.DeleteCountryCommand, id=result.id + 1)

    with pytest.raises(EmptyResult):
        await country_repository.delete(cmd=cmd)
