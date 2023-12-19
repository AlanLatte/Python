import pytest

from app.internal.repository.postgresql import ContactsRepository
from app.pkg import models
from app.pkg.models.exceptions.repository import EmptyResult


@pytest.mark.postgresql
async def test_delete(
    contact_repository: ContactsRepository,
    contact_inserter,
    partner_inserter,
):
    partner, _ = await partner_inserter()
    contact, _ = await contact_inserter(partner_id=partner.id)

    await contact_repository.delete(
        cmd=contact.migrate(model=models.DeleteContactsCommand),
    )

    with pytest.raises(EmptyResult):
        await contact_repository.read_by_telegram_user_id(
            query=models.ReadContactsByTelegramUserIdQuery(
                telegram_user_id=contact.telegram_user_id,
            ),
        )


@pytest.mark.postgresql
async def test_delete_not_found(
    contact_repository: ContactsRepository, contact_generator
):
    cmd = contact_generator().migrate(model=models.DeleteContactsCommand)
    with pytest.raises(EmptyResult):
        await contact_repository.delete(cmd=cmd)
