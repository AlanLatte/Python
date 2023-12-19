"""Repository for contacts."""

from typing import List

from app.internal.repository.postgresql.connection import get_connection
from app.internal.repository.postgresql.handlers.collect_response import (
    collect_response,
)
from app.internal.repository.repository import Repository
from app.pkg import models

__all__ = ["ContactsRepository"]


class ContactsRepository(Repository):
    """Contacts repository implementation."""

    @collect_response
    async def create(self, cmd: models.CreateContactsCommand) -> models.Contacts:
        q = """
            insert into contacts(
                token,
                email,
                telegram_username,
                telegram_user_id,
                partner_id
            ) values (
                %(token)s, %(email)s, %(telegram_username)s,
                %(telegram_user_id)s, %(partner_id)s
            )
            returning id, token, email, telegram_username, telegram_user_id, partner_id
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict(show_secrets=True))
            return await cur.fetchone()

    @collect_response
    async def read(self, query: models.ReadContactsQuery) -> models.Contacts:
        q = """
            select
                id,
                token,
                email,
                telegram_username,
                telegram_user_id,
                partner_id
            from contacts
            where token = %(token)s
        """
        async with get_connection() as cur:
            await cur.execute(q, query.to_dict(show_secrets=True))
            return await cur.fetchone()

    @collect_response
    async def read_by_telegram_user_id(
        self,
        query: models.ReadContactsByTelegramUserIdQuery,
    ) -> models.Contacts:
        q = """
            select
                id,
                token,
                email,
                telegram_username,
                telegram_user_id,
                partner_id
            from contacts
            where telegram_user_id = %(telegram_user_id)s
        """
        async with get_connection() as cur:
            await cur.execute(q, query.to_dict())
            return await cur.fetchone()

    @collect_response
    async def read_by_id(self, query: models.ReadContactsByIdQuery) -> models.Contacts:
        q = """
            select
                id,
                token,
                email,
                telegram_username,
                telegram_user_id,
                partner_id
            from contacts
            where id = %(id)s
        """
        async with get_connection() as cur:
            await cur.execute(q, query.to_dict())
            return await cur.fetchone()

    @collect_response
    async def read_all(self) -> List[models.Contacts]:
        q = """
            select
                id,
                token,
                email,
                telegram_username,
                telegram_user_id,
                partner_id
            from contacts
        """
        async with get_connection() as cur:
            await cur.execute(q)
            return await cur.fetchall()

    @collect_response
    async def update(self, cmd: models.UpdateContactsCommand) -> models.Contacts:
        q = """
            update contacts
            set
                email = %(email)s,
                telegram_username = %(telegram_username)s,
                token = %(token)s
            where telegram_user_id = %(telegram_user_id)s
            returning id, token, email, telegram_username, telegram_user_id, partner_id
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict(show_secrets=True))
            return await cur.fetchone()

    @collect_response
    async def delete(self, cmd: models.DeleteContactsCommand) -> models.Contacts:
        q = """
            delete from contacts
            where id = %(id)s
            returning id, token, email, telegram_username, telegram_user_id, partner_id
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()
