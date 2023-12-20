"""Module for testing read_by_id method in ContactsRepository."""


import pytest

from app.internal.repository.postgresql import ContactsRepository
from app.pkg import models
from app.pkg.models.exceptions.repository import EmptyResult


@pytest.mark.postgresql
async def test_read_by_id(
    contact_repository: ContactsRepository,
    contact_inserter,
    partner_inserter,
):
    partner, _ = await partner_inserter()
    contact, _ = await contact_inserter(partner_id=partner.id)

    result = await contact_repository.read_by_id(
        query=models.ReadContactsByIdQuery(
            id=contact.id,
        ),
    )

    assert result == contact.migrate(model=models.Contacts)


@pytest.mark.postgresql
async def test_read_by_id_not_found(
    contact_repository: ContactsRepository,
    contact_inserter,
    partner_inserter,
):
    partner, _ = await partner_inserter()
    contact, _ = await contact_inserter(partner_id=partner.id)

    with pytest.raises(EmptyResult):
        await contact_repository.read_by_id(
            query=models.ReadContactsByIdQuery(
                id=contact.id + 1,
            ),
        )
