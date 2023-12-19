import pytest

from app.internal.repository.postgresql import ContactsRepository
from app.pkg import models
from app.pkg.models.exceptions.contacts import ContactsNotFound
from app.pkg.models.exceptions.repository import EmptyResult


@pytest.mark.postgresql
async def test_read(
    contact_repository: ContactsRepository,
    contact_inserter,
    partner_inserter,
):
    partner, _ = await partner_inserter()
    contact, _ = await contact_inserter(partner_id=partner.id)

    result = await contact_repository.read(
        query=models.ReadContactsQuery(token=contact.token),
    )

    assert result == contact.migrate(model=models.Contacts)


@pytest.mark.postgresql
async def test_read_not_found(
    contact_repository: ContactsRepository,
    contact_inserter,
    partner_inserter,
):
    partner, _ = await partner_inserter()
    contact, _ = await contact_inserter(partner_id=partner.id)

    with pytest.raises(EmptyResult):
        await contact_repository.read(
            query=models.ReadContactsQuery(
                token=contact.token.get_secret_value() + "1"
            ),
        )
