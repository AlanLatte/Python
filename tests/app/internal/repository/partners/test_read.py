import pytest

from app.pkg import models
from app.pkg.models.exceptions.repository import EmptyResult


@pytest.mark.postgresql
async def test_read(partner_inserter, partner_repository):
    partner, _ = await partner_inserter()
    result = await partner_repository.read(
        query=partner.migrate(models.ReadPartnerQuery),
    )
    assert result == partner


@pytest.mark.postgresql
async def test_read_not_found(partner_repository):
    with pytest.raises(EmptyResult):
        await partner_repository.read(query=models.ReadPartnerQuery(id=1))


@pytest.mark.postgresql
async def test_read_by_token(partner_inserter, partner_repository):
    partner, _ = await partner_inserter()
    result = await partner_repository.read_by_token(
        query=partner.migrate(models.ReadPartnerByTokenQuery),
    )
    assert result == partner


@pytest.mark.postgresql
async def test_read_by_token_not_found(partner_repository):
    with pytest.raises(EmptyResult):
        await partner_repository.read_by_token(
            query=models.ReadPartnerByTokenQuery(token="token"),
        )
