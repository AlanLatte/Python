"""Module for testing update direction repository method."""


import pytest

from app.pkg.models.exceptions.repository import EmptyResult


@pytest.mark.postgresql
@pytest.mark.slow
async def test_read_all(direction_repository, direction_inserter, clean_postgres):
    _ = clean_postgres

    result, _ = await direction_inserter()

    assert await direction_repository.read_all() == [result]


@pytest.mark.postgresql
@pytest.mark.slow
async def test_direction_not_found(direction_repository, clean_postgres):
    _ = clean_postgres

    with pytest.raises(EmptyResult):
        await direction_repository.read_all()
