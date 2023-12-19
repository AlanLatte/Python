"""Module for testing update method of contacts repository."""


import uuid

import pytest

from app.internal.repository.postgresql import ContactsRepository
from app.pkg import models
from app.pkg.models.exceptions.contacts import (
    EmailAlreadyExists,
    TelegramUsernameAlreadyExists,
    TokenAlreadyExists,
)
from app.pkg.models.exceptions.repository import EmptyResult


@pytest.mark.postgresql
async def test_update(
    contact_repository: ContactsRepository,
    contact_inserter,
    partner_inserter,
):
    partner, _ = await partner_inserter()
    contact, _ = await contact_inserter(
        partner_id=partner.id,
        telegram_username=f"@{uuid.uuid4().hex}",
    )
    new_contact = contact.migrate(
        model=models.Contacts,
        extra_fields={"telegram_username": contact.telegram_username + "1"},
    )

    result = await contact_repository.update(
        cmd=new_contact.migrate(model=models.UpdateContactsCommand),
    )

    assert result == new_contact


@pytest.mark.postgresql
async def test_token_already_exists(
    contact_repository: ContactsRepository,
    contact_inserter,
    partner_inserter,
    create_model,
):
    partner, _ = await partner_inserter()
    contact, _ = await contact_inserter(partner_id=partner.id)

    new_contact = await create_model(
        models.Contacts,
        telegram_user_id=contact.telegram_user_id,
        token=str(uuid.uuid4()),
    )

    _, cmd = await contact_inserter(partner_id=partner.id, token=new_contact.token)

    with pytest.raises(TokenAlreadyExists):
        await contact_repository.update(
            cmd=contact.migrate(
                model=models.UpdateContactsCommand,
                extra_fields={"token": cmd.token},
            ),
        )


@pytest.mark.postgresql
async def test_email_already_exists(
    contact_repository: ContactsRepository,
    contact_inserter,
    partner_inserter,
    create_model,
):
    partner, _ = await partner_inserter()
    contact, _ = await contact_inserter(partner_id=partner.id)

    new_contact = await create_model(
        models.Contacts,
        telegram_user_id=contact.telegram_user_id,
        email=f"{uuid.uuid4().hex}@{uuid.uuid4().hex}.com",
    )

    _, cmd = await contact_inserter(partner_id=partner.id, email=new_contact.email)

    with pytest.raises(EmailAlreadyExists):
        await contact_repository.update(
            cmd=contact.migrate(
                model=models.UpdateContactsCommand,
                extra_fields={"email": cmd.email},
            ),
        )


@pytest.mark.postgresql
async def test_telegram_username_already_exists(
    contact_repository: ContactsRepository,
    contact_inserter,
    partner_inserter,
    create_model,
):
    partner, _ = await partner_inserter()
    contact, _ = await contact_inserter(
        partner_id=partner.id,
        telegram_username=f"@{uuid.uuid4().hex}",
    )

    new_contact = await create_model(
        models.Contacts,
        telegram_username=f"@{uuid.uuid4().hex}",
    )

    _, cmd = await contact_inserter(
        partner_id=partner.id,
        telegram_username=new_contact.telegram_username,
    )

    with pytest.raises(TelegramUsernameAlreadyExists):
        await contact_repository.update(
            cmd=contact.migrate(
                model=models.UpdateContactsCommand,
                extra_fields={"telegram_username": cmd.telegram_username},
            ),
        )


@pytest.mark.postgresql
async def test_update_not_found(
    contact_repository: ContactsRepository,
    contact_inserter,
    partner_inserter,
):
    partner, _ = await partner_inserter()
    contact, _ = await contact_inserter(partner_id=partner.id)

    with pytest.raises(EmptyResult):
        await contact_repository.update(
            cmd=contact.migrate(
                model=models.UpdateContactsCommand,
                extra_fields={"telegram_user_id": contact.telegram_user_id + 1},
            ),
        )
