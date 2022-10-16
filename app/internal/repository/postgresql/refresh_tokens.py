from typing import List

from app.internal.repository.postgresql.handlers.collect_response import collect_response
from app.internal.repository.repository import Repository
from app.pkg.models.base import Model
from app.pkg.models.refresh_token import (
    CreateJWTTokenCommand,
    DeleteJWTTokenCommand,
    JWTToken,
    ReadJWTTokenQuery,
    ReadJWTTokenQueryByFingerprint,
    UpdateJWTTokenCommand,
)

from .connection import get_connection


class RefreshTokenRepository(Repository):
    @collect_response
    async def create(self, cmd: CreateJWTTokenCommand) -> JWTToken:
        q = """
                insert into refresh_tokens(user_id, refresh_token, fingerprint)
                    values (%(user_id)s, %(refresh_token)s, %(fingerprint)s)
                returning *;
            """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict(show_secrets=True))
            return await cur.fetchone()

    @collect_response
    async def read(self, query: ReadJWTTokenQuery) -> JWTToken:
        q = """
                select user_id, refresh_token, fingerprint from refresh_tokens
                where user_id = %(user_id)s and refresh_token = %(refresh_token)s;
            """
        async with get_connection() as cur:
            await cur.execute(q, query.to_dict(show_secrets=True))
            return await cur.fetchone()

    @collect_response
    async def read_by_fingerprint(
        self,
        query: ReadJWTTokenQueryByFingerprint,
    ) -> JWTToken:
        q = """
                select user_id, refresh_token, fingerprint from refresh_tokens
                where user_id = %(user_id)s and fingerprint = %(fingerprint)s;
            """
        async with get_connection() as cur:
            await cur.execute(q, query.to_dict(show_secrets=True))
            return await cur.fetchone()

    async def read_all(self) -> List[Model]:
        raise NotImplementedError

    @collect_response
    async def update(self, cmd: UpdateJWTTokenCommand) -> JWTToken:
        q = """
                update refresh_tokens set refresh_token = %(refresh_token)s
                    where user_id = %(user_id)s and fingerprint = %(fingerprint)s
                returning *;
            """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict(show_secrets=True))
            return await cur.fetchone()

    @collect_response
    async def delete(self, cmd: DeleteJWTTokenCommand) -> JWTToken:
        q = """
                delete from refresh_tokens
                    where user_id = %(user_id)s and fingerprint = %(fingerprint)s
                returning *;
            """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict(show_secrets=True))
            return await cur.fetchone()
