import pytest

from app.internal.repository.postgresql import (
    ContactsRepository,
)

from app.pkg import models
from app.pkg.models.exceptions.repository import EmptyResult


@pytest.mark.postgresql
@pytest.mark.slow
async def test_read_all(
    contact_repository: ContactsRepository,
    contact_inserter,
    partner_inserter,
):
    partner, _ = await partner_inserter()
    contact, _ = await contact_inserter(partner_id=partner.id)

    result = await contact_repository.read_all()

    assert result == [
        contact.migrate(model=models.Contacts),
    ]


@pytest.mark.postgresql
@pytest.mark.slow
async def test_read_all_not_found(
    contact_repository: ContactsRepository, clean_postgres
):
    _ = clean_postgres

    with pytest.raises(EmptyResult):
        await contact_repository.read_all()
