"""Exceptions for contacts module."""

from starlette import status

from app.pkg.models.base import BaseAPIException

__all__ = [
    "EmailAlreadyExists",
    "TelegramIdAlreadyExists",
    "PartnerForContactNotFound",
    "TelegramUsernameAlreadyExists",
    "TokenAlreadyExists",
    "ContactsNotFound",
    "EmailNotChanged",
]


class ContactsNotFound(BaseAPIException):
    message = "Contact not found."
    status_code = status.HTTP_404_NOT_FOUND


class EmailAlreadyExists(BaseAPIException):
    message = "This 'email' already exists."
    status_code = status.HTTP_409_CONFLICT


class TelegramIdAlreadyExists(BaseAPIException):
    message = "This 'telegram_id' already exists."
    status_code = status.HTTP_409_CONFLICT


class TelegramUsernameAlreadyExists(BaseAPIException):
    message = "This 'telegram_username' already exists."
    status_code = status.HTTP_409_CONFLICT


class EmailNotChanged(BaseAPIException):
    message = "Email not changed."
    status_code = status.HTTP_304_NOT_MODIFIED


class PartnerForContactNotFound(BaseAPIException):
    message = "Partner not found."
    status_code = status.HTTP_404_NOT_FOUND


class TokenAlreadyExists(BaseAPIException):
    message = "This 'token' already exists."
    status_code = status.HTTP_409_CONFLICT


__constrains__ = {
    "contacts_email_key": EmailAlreadyExists,
    "contacts_telegram_user_id_key": TelegramIdAlreadyExists,
    "contacts_telegram_username_key": TelegramUsernameAlreadyExists,
    "contacts_partner_id_fkey": PartnerForContactNotFound,
    "contacts_token_key": TokenAlreadyExists,
}
