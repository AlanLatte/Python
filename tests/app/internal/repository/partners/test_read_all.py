import pytest

from app.internal.repository.postgresql import PartnerRepository
from app.pkg.models.exceptions.repository import EmptyResult


@pytest.mark.postgresql
@pytest.mark.slow
async def test_read_all(
    partner_inserter, partner_repository: PartnerRepository, clean_postgres,
):
    _ = clean_postgres

    partner, _ = await partner_inserter()
    result = await partner_repository.read_all()
    assert result == [partner]


@pytest.mark.postgresql
@pytest.mark.slow
async def test_read_all_not_found(
    partner_repository: PartnerRepository, clean_postgres,
):
    _ = clean_postgres

    with pytest.raises(EmptyResult):
        await partner_repository.read_all()
