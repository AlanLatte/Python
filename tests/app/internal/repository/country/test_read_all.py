import pytest

from app.pkg.models.exceptions.repository import EmptyResult


@pytest.mark.postgresql
@pytest.mark.slow
async def test_read_all(country_repository, country_inserter, clean_postgres):
    _ = clean_postgres

    result, _ = await country_inserter()

    assert await country_repository.read_all() == [result]


@pytest.mark.postgresql
@pytest.mark.slow
async def test_country_not_found(country_repository, clean_postgres):
    _ = clean_postgres

    with pytest.raises(EmptyResult):
        await country_repository.read_all()
