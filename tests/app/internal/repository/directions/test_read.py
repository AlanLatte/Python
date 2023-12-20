"""Module for testing delete city repository method."""


import pytest

from app.internal.repository.postgresql import CountryRepository, DirectionRepository
from app.pkg import models
from app.pkg.models.exceptions.repository import EmptyResult


@pytest.mark.postgresql
async def test_read(
    country_repository: CountryRepository,
    country_inserter,
):
    expected, _ = await country_inserter()

    result = await country_repository.read(
        query=models.ReadCountryQuery(id=expected.id),
    )
    assert result == expected


@pytest.mark.postgresql
async def test_country_not_found(
    direction_repository: DirectionRepository,
    direction_inserter,
):
    expected, _ = await direction_inserter()
    query = expected.migrate(
        models.ReadDirectionQuery,
        extra_fields={"id": expected.id + 1},
    )

    with pytest.raises(EmptyResult):
        await direction_repository.read(query=query)
