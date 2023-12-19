"""Module for testing delete method of PartnerRepository."""


import pytest

from app.internal.repository.postgresql import PartnerRepository
from app.pkg import models
from app.pkg.models.exceptions.repository import EmptyResult


@pytest.mark.postgresql
async def test_delete(partner_inserter, partner_repository: PartnerRepository):
    partner, _ = await partner_inserter()

    result = await partner_repository.delete(
        cmd=models.DeletePartnerCommand(id=partner.id),
    )

    assert result == partner

    with pytest.raises(EmptyResult):
        await partner_repository.read(query=models.ReadPartnerQuery(id=partner.id))


@pytest.mark.postgresql
async def test_delete_not_found(
    partner_repository: PartnerRepository,
    partner_inserter,
):
    partner, _ = await partner_inserter()

    with pytest.raises(EmptyResult):
        await partner_repository.delete(
            cmd=models.DeletePartnerCommand(id=partner.id + 1),
        )
