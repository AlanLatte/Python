"""Model tests for the create method of the partner repository."""


import uuid

import pytest

from app.pkg import models
from app.pkg.models.exceptions.partners import (
    PartnerNameAlreadyExists,
    PartnerTokenAlreadyExists,
)


@pytest.mark.postgresql
async def test_create(partner_generator, partner_repository):
    partner = partner_generator()
    cmd = partner.migrate(model=models.CreatePartnerCommand)

    result = await partner_repository.create(cmd=cmd)

    assert result == partner.migrate(
        model=models.Partner,
        extra_fields={"id": result.id},
    )


@pytest.mark.postgresql
async def test_unique_name(partner_generator, partner_repository):
    partner = partner_generator()
    cmd = partner.migrate(model=models.CreatePartnerCommand)

    await partner_repository.create(cmd=cmd)

    with pytest.raises(PartnerNameAlreadyExists):
        await partner_repository.create(cmd=cmd)


@pytest.mark.postgresql
async def test_unique_token(partner_generator, partner_repository):
    partner = partner_generator()
    token = str(uuid.uuid4())
    cmd = partner.migrate(
        model=models.CreatePartnerCommand,
        extra_fields={"token": token},
    )

    await partner_repository.create(cmd=cmd)

    with pytest.raises(PartnerTokenAlreadyExists):
        await partner_repository.create(
            cmd=partner.migrate(
                models.CreatePartnerCommand,
                extra_fields={"token": token, "name": str(uuid.uuid4())},
            ),
        )


@pytest.mark.postgresql
async def test_default_token_generator(partner_repository):
    cmd = models.CreatePartnerCommand(name=str(uuid.uuid4()))

    result = await partner_repository.create(cmd=cmd)

    assert result.token is not None
    assert len(result.token) == 8
