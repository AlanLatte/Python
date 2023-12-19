"""Module for testing create method of contacts repository."""

from uuid import uuid4

import pytest

from app.internal.repository.postgresql import ContactsRepository
from app.pkg import models
from app.pkg.models.exceptions.contacts import (
    EmailAlreadyExists,
    PartnerForContactNotFound,
    TelegramIdAlreadyExists,
    TelegramUsernameAlreadyExists,
    TokenAlreadyExists,
)


@pytest.mark.postgresql
async def test_create(
    contact_repository: ContactsRepository,
    contact_generator,
    partner_inserter,
):
    partner, _ = await partner_inserter()

    contact = contact_generator(partner_id=partner.id)

    cmd = contact.migrate(model=models.CreateContactsCommand)

    result = await contact_repository.create(cmd=cmd)

    assert result == contact.migrate(
        model=models.Contacts,
        extra_fields={"id": result.id},
    )


@pytest.mark.postgresql
async def test_unrequired_email(
    contact_repository: ContactsRepository,
    contact_generator,
    partner_inserter,
):
    partner, _ = await partner_inserter()
    contact = contact_generator(email=None, partner_id=partner.id)

    cmd = contact.migrate(model=models.CreateContactsCommand)

    result = await contact_repository.create(cmd=cmd)

    assert result == contact.migrate(
        model=models.Contacts,
        extra_fields={"id": result.id},
    )


@pytest.mark.postgresql
async def test_unrequired_partner_id(
    contact_repository: ContactsRepository,
    contact_generator,
):
    contact = contact_generator(partner_id=None)

    cmd = contact.migrate(model=models.CreateContactsCommand)

    result = await contact_repository.create(cmd=cmd)

    assert result == contact.migrate(
        model=models.Contacts,
        extra_fields={"id": result.id},
    )


@pytest.mark.postgresql
async def test_duplicate_email(
    contact_repository: ContactsRepository,
    contact_inserter,
    partner_inserter,
    contact_generator,
):
    partner, _ = await partner_inserter()
    contact, _ = await contact_inserter(
        partner_id=partner.id,
        email=f"{uuid4().hex}@example.com",
        token=uuid4().hex,
    )

    cmd = contact_generator(partner_id=partner.id, email=contact.email).migrate(
        model=models.CreateContactsCommand,
    )

    with pytest.raises(EmailAlreadyExists):
        await contact_repository.create(cmd=cmd)


@pytest.mark.postgresql
async def test_duplicate_telegram_username(
    contact_repository: ContactsRepository,
    contact_inserter,
    partner_inserter,
    contact_generator,
):
    partner, _ = await partner_inserter()
    contact, _ = await contact_inserter(
        partner_id=partner.id,
        telegram_username=f"@{uuid4().hex}",
        email=None,
    )

    cmd = contact_generator(
        partner_id=partner.id,
        telegram_username=contact.telegram_username,
    ).migrate(model=models.CreateContactsCommand)

    with pytest.raises(TelegramUsernameAlreadyExists):
        await contact_repository.create(cmd=cmd)


@pytest.mark.postgresql
async def test_duplicate_telegram_id(
    contact_repository: ContactsRepository,
    contact_inserter,
    partner_inserter,
    contact_generator,
):
    partner, _ = await partner_inserter()
    contact, _ = await contact_inserter(partner_id=partner.id)

    cmd = contact_generator(
        partner_id=partner.id,
        telegram_user_id=contact.telegram_user_id,
    ).migrate(model=models.CreateContactsCommand)

    with pytest.raises(TelegramIdAlreadyExists):
        await contact_repository.create(cmd=cmd)


@pytest.mark.postgresql
async def test_unknown_partner(
    contact_repository: ContactsRepository,
    contact_generator,
    partner_inserter,
):
    partner, _ = await partner_inserter()
    contact = contact_generator(partner_id=partner.id + 1)

    cmd = contact.migrate(model=models.CreateContactsCommand)

    with pytest.raises(PartnerForContactNotFound):
        await contact_repository.create(cmd=cmd)


@pytest.mark.postgresql
async def test_token_already_exists(
    contact_repository: ContactsRepository,
    contact_inserter,
    partner_inserter,
    contact_generator,
):
    partner, _ = await partner_inserter()
    contact, _ = await contact_inserter(partner_id=partner.id)

    cmd = contact_generator(partner_id=partner.id, token=contact.token).migrate(
        model=models.CreateContactsCommand,
    )

    with pytest.raises(TokenAlreadyExists):
        await contact_repository.create(cmd=cmd)
