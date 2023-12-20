"""Service for manage contacts."""


import typing

from pydantic.types import SecretStr

from app.internal.repository.postgresql import contacts
from app.internal.repository.repository import BaseRepository
from app.pkg import models
from app.pkg.models.exceptions.contacts import ContactsNotFound, EmailNotChanged
from app.pkg.models.exceptions.repository import EmptyResult

__all__ = ["ContactsService"]


class ContactsService:
    """Service for manage contacts."""

    #: ContactsRepository: ContactsRepository repository implementation.
    repository: contacts.ContactsRepository

    def __init__(self, contacts_repository: BaseRepository):
        self.repository = contacts_repository

    async def create_contacts(
        self,
        cmd: models.CreateContactsCommand,
    ) -> models.Contacts:
        """Create contacts.

        Args:
            cmd: CreateContactsCommand command.

        Returns:
            Contacts: Created contacts.
        """
        return await self.repository.create(cmd=cmd)

    async def read_contacts_by_telegram_user_id(
        self,
        query: models.ReadContactsByTelegramUserIdQuery,
    ) -> models.Contacts:
        """Read contacts by telegram user id.

        Args:
            query: ReadContactsQuery query.

        Returns:
            Contacts: Read contacts.
        """
        try:
            return await self.repository.read_by_telegram_user_id(query=query)
        except EmptyResult as e:
            raise ContactsNotFound from e

    async def read_contacts_by_id(
        self,
        query: models.ReadContactsByIdQuery,
    ) -> models.Contacts:
        """Read contacts by id.

        Args:
            query: ReadContactsQuery query.

        Returns:
            Contacts: Read contacts.
        """
        try:
            return await self.repository.read_by_id(query=query)
        except EmptyResult as e:
            raise ContactsNotFound from e

    async def read_by_token(self, query: models.ReadContactsQuery) -> models.Contacts:
        """Read contacts by token.

        Args:
            query: ReadContactsQuery query.

        Returns:
            Contacts: Read contacts.
        """
        try:
            return await self.repository.read(query=query)
        except EmptyResult as e:
            raise ContactsNotFound from e

    async def read_all_contacts(self) -> typing.List[models.Contacts]:
        """Read all contacts.

        Returns:
            List[Contacts]: Read all contacts.
        """
        try:
            return await self.repository.read_all()
        except EmptyResult as e:
            raise ContactsNotFound from e

    async def update_contacts(
        self,
        token: SecretStr,
        cmd: models.UpdateEmailCommand,
    ) -> models.Contacts:
        """Update contacts.

        Args:
            token: Contacts token.
            cmd: UpdateContactsCommand command.

        Returns:
            Contacts: Updated contacts.
        """
        try:
            token_holder = await self.read_by_token(
                query=models.ReadContactsQuery(token=token),
            )
        except EmptyResult as e:
            raise ContactsNotFound from e
        else:
            if token_holder.email == cmd.email:
                raise EmailNotChanged
            token_holder.email = cmd.email

            return await self.repository.update(
                cmd=token_holder.migrate(models.UpdateContactsCommand),
            )

    async def delete_contacts(
        self,
        cmd: models.DeleteContactsCommand,
    ) -> models.Contacts:
        """Delete contacts.

        Args:
            cmd: DeleteContactsCommand command.
        """
        return await self.repository.delete(cmd=cmd)
