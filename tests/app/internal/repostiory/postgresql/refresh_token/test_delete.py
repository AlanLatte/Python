import uuid

import pytest

from app.pkg import models
from app.internal.repository.postgresql.refresh_tokens import JWTRefreshTokenRepository
from app.pkg.models.exceptions.repository import DriverError, EmptyResult


async def test_correct(
    refresh_token_repository: JWTRefreshTokenRepository,
    insert_first_refresh_token: models.JWTRefreshToken,
    insert_first_user: models.User,
    first_fingerprint: str,
    first_refresh_token: str,
):
    response = await refresh_token_repository.delete(
        cmd=models.DeleteJWTRefreshTokenCommand(
            user_id=insert_first_user.id,
            fingerprint=first_fingerprint,
            refresh_token=first_refresh_token,
        )
    )

    assert response == models.JWTRefreshToken(
        user_id=insert_first_user.id,
        fingerprint=first_fingerprint,
        refresh_token=first_refresh_token,
    )


@pytest.mark.parametrize(
    "user_id,fingerprint,refresh_token",
    [
        [1, uuid.uuid4().__str__(), uuid.uuid4().__str__()],
        [2, uuid.uuid4().__str__(), uuid.uuid4().__str__()],
        [3, uuid.uuid4().__str__(), uuid.uuid4().__str__()],
        [4, uuid.uuid4().__str__(), uuid.uuid4().__str__()],
    ],
)
async def test_user_does_exist(
    refresh_token_repository: JWTRefreshTokenRepository,
    user_id: int,
    fingerprint: str,
    refresh_token: str,
):
    with pytest.raises(DriverError):
        await refresh_token_repository.create(
            cmd=models.CreateJWTRefreshTokenCommand(
                user_id=user_id,
                refresh_token=refresh_token,
                fingerprint=fingerprint,
            )
        )


@pytest.mark.parametrize(
    "fingerprint,refresh_token",
    [
        [uuid.uuid4().__str__(), uuid.uuid4().__str__()],
        [uuid.uuid4().__str__(), uuid.uuid4().__str__()],
        [uuid.uuid4().__str__(), uuid.uuid4().__str__()],
    ],
)
async def test_not_exist(
    refresh_token_repository: JWTRefreshTokenRepository,
    insert_first_user: models.User,
    fingerprint: str,
    refresh_token: str,
):
    with pytest.raises(EmptyResult):
        await refresh_token_repository.delete(
            cmd=models.DeleteJWTRefreshTokenCommand(
                user_id=insert_first_user.id,
                fingerprint=fingerprint,
                refresh_token=refresh_token,
            )
        )
