"""Models of contacts."""

import typing
import uuid

from pydantic import EmailStr
from pydantic.fields import Field
from pydantic.types import PositiveInt, SecretStr

from app.pkg.models.base import BaseModel

__all__ = [
    "Contacts",
    "ContactsFields",
    "CreateContactsCommand",
    "ReadContactsQuery",
    "ReadContactsByIdQuery",
    "ReadContactsByTelegramUserIdQuery",
    "UpdateContactsCommand",
    "UpdateEmailCommand",
    "DeleteContactsCommand",
]


class BaseContacts(BaseModel):
    """Base model for contacts."""


class ContactsFields:
    """Model fields of contacts."""

    id: PositiveInt = Field(description="Internal skill id.", example=1)
    email: typing.Optional[EmailStr] = Field(
        description="StrictUser email.",
        example="test@example.ru",
        default=None,
    )
    telegram_username: typing.Optional[str] = Field(
        description="Telegram username.",
        example="@tester1337",
        default=None,
        regex=r"^@[\w\d_]{5,}$",
    )
    token: SecretStr = Field(
        description="Personal token.",
        example="0418e076-be66-4ccc-9503-991ee89d2208",
        default_factory=uuid.uuid4,
    )
    telegram_user_id: PositiveInt = Field(
        description="Telegram user id.",
        example=123456789,
    )
    partner_id: typing.Optional[PositiveInt] = Field(
        description="Partner id.",
        example=1,
        default=None,
    )


class _Contacts(BaseContacts):
    email: typing.Optional[EmailStr] = ContactsFields.email
    telegram_username: typing.Optional[str] = ContactsFields.telegram_username
    token: SecretStr = ContactsFields.token
    telegram_user_id: PositiveInt = ContactsFields.telegram_user_id
    partner_id: typing.Optional[PositiveInt] = ContactsFields.partner_id


class Contacts(_Contacts):
    id: PositiveInt = ContactsFields.id


# Commands.
class CreateContactsCommand(_Contacts):
    ...


class UpdateContactsCommand(_Contacts):
    id: PositiveInt = ContactsFields.id


class UpdateEmailCommand(BaseContacts):
    email: typing.Optional[EmailStr] = ContactsFields.email


class DeleteContactsCommand(BaseContacts):
    id: PositiveInt = ContactsFields.id


# Queries.
class ReadContactsQuery(BaseContacts):
    token: SecretStr = ContactsFields.token


class ReadContactsByTelegramUserIdQuery(BaseContacts):
    telegram_user_id: PositiveInt = ContactsFields.telegram_user_id


class ReadContactsByIdQuery(BaseContacts):
    id: PositiveInt = ContactsFields.id
