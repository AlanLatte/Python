import pytest

from app.internal.repository.postgresql import ContactsRepository
from app.pkg import models
from app.pkg.models.exceptions.repository import EmptyResult


@pytest.mark.postgresql
async def test_read_by_telegram_user_id(
    contact_repository: ContactsRepository,
    contact_inserter,
    partner_inserter,
):
    partner, _ = await partner_inserter()
    contact, _ = await contact_inserter(partner_id=partner.id)

    result = await contact_repository.read_by_telegram_user_id(
        query=models.ReadContactsByTelegramUserIdQuery(
            telegram_user_id=contact.telegram_user_id,
        ),
    )

    assert result == contact.migrate(model=models.Contacts)


@pytest.mark.postgresql
async def test_read_by_telegram_user_id_not_found(
    contact_repository: ContactsRepository,
    contact_inserter,
    partner_inserter,
):
    partner, _ = await partner_inserter()
    contact, _ = await contact_inserter(partner_id=partner.id)

    with pytest.raises(EmptyResult):
        await contact_repository.read_by_telegram_user_id(
            query=models.ReadContactsByTelegramUserIdQuery(
                telegram_user_id=contact.telegram_user_id + 1,
            ),
        )
