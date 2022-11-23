from typing import List

from app.internal.repository.postgresql.handlers.collect_response import \
    collect_response
from app.internal.repository.postgresql.connection import get_connection
from app.internal.repository.repository import Repository
from app.pkg import models

__all__ = ["UserRepository"]


class UserRepository(Repository):
    @collect_response
    async def create(self, cmd: models.CreateUserCommand) -> models.User:
        q = """
            insert into users(
                username, password, role_id
            ) values (
                %(username)s,
                %(password)s::bytea,
                (select id from user_roles where role_name = %(role_name)s)
            )
            returning id, username, password, (
                select role_name from user_roles where role_name = %(role_name)s
            );
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict(show_secrets=True))
            return await cur.fetchone()

    @collect_response
    async def read(self, query: models.ReadUserByIdQuery) -> models.User:
        q = """
            select
                users.id,
                username,
                password,
                ur.role_name
            from users
                left join user_roles ur on ur.id = users.role_id
            where users.id = %(id)s;
        """
        async with get_connection() as cur:
            await cur.execute(q, query.to_dict(show_secrets=True))
            return await cur.fetchone()

    @collect_response(nullable=True)
    async def read_by_username(
        self,
        query: models.ReadUserByUserNameQuery,
    ) -> models.User:
        q = """
            select
                users.id, username, password, ur.role_name as role_name
            from users
                left join user_roles ur on ur.id = users.role_id
            where username = %(username)s
        """
        async with get_connection() as cur:
            await cur.execute(q, query.to_dict(show_secrets=True))
            return await cur.fetchone()

    @collect_response(nullable=True)
    async def read_all(self) -> List[models.User]:
        q = """
            select
                users.id,
                username,
                password,
                ur.role_name as role_name
            from users
                left join user_roles ur on ur.id = users.role_id;
        """
        async with get_connection() as cur:
            await cur.execute(q)
            return await cur.fetchall()

    @collect_response
    async def update(self, cmd: models.UpdateUserCommand) -> models.User:
        q = """
            with ur as (
                select id, role_name from user_roles where role_name = %(role_name)s
            )
            update users
                set
                    username = %(username)s,
                    password = %(password)s,
                    role_id = (select id from ur),
                    password_updated_at = current_timestamp
                where id = %(id)s
            returning
                id, username, password,
                (select role_name from ur);
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict(show_secrets=True))
            return await cur.fetchone()

    @collect_response
    async def delete(self, cmd: models.DeleteUserCommand) -> models.User:
        q = """
            delete from users where id = %(id)s
            returning id, username, password, (
                select role_name from user_roles
                    where id=users.role_id
            );
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict(show_secrets=True))
            return await cur.fetchone()
