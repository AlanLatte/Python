"""Module for testing update method of partner repository."""


from uuid import uuid4

import pytest

from app.internal.repository.postgresql import PartnerRepository
from app.pkg import models
from app.pkg.models.exceptions.partners import (
    PartnerNameAlreadyExists,
    PartnerTokenAlreadyExists,
)
from app.pkg.models.exceptions.repository import EmptyResult


@pytest.mark.postgresql
async def test_update(partner_inserter, partner_repository: PartnerRepository):
    partner, _ = await partner_inserter()

    cmd = partner.migrate(
        model=models.UpdatePartnerCommand,
        extra_fields={"id": partner.id, "name": uuid4().hex, "token": uuid4().hex},
    )

    result = await partner_repository.update(cmd=cmd)

    assert result == cmd.migrate(
        model=models.Partner,
        extra_fields={"id": result.id},
    )


@pytest.mark.postgresql
async def test_update_not_found(partner_repository: PartnerRepository):
    cmd = models.UpdatePartnerCommand(
        id=uuid4(),
        name=uuid4().hex,
        token=uuid4().hex,
    )

    with pytest.raises(EmptyResult):
        await partner_repository.update(cmd=cmd)


@pytest.mark.postgresql
async def test_update_duplicate_name(
    partner_inserter,
    partner_repository: PartnerRepository,
):
    partner, _ = await partner_inserter()
    partner2, _ = await partner_inserter()

    cmd = partner.migrate(
        model=models.UpdatePartnerCommand,
        extra_fields={"id": partner.id, "name": partner2.name, "token": uuid4().hex},
    )

    with pytest.raises(PartnerNameAlreadyExists):
        await partner_repository.update(cmd=cmd)


@pytest.mark.postgresql
async def test_update_duplicate_token(
    partner_inserter,
    partner_repository: PartnerRepository,
):
    partner, _ = await partner_inserter()
    partner2, _ = await partner_inserter()

    cmd = partner.migrate(
        model=models.UpdatePartnerCommand,
        extra_fields={"id": partner.id, "name": uuid4().hex, "token": partner2.token},
    )

    with pytest.raises(PartnerTokenAlreadyExists):
        await partner_repository.update(cmd=cmd)
