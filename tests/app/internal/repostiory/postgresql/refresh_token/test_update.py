import uuid

import pytest

from app.internal.repository.postgresql import JWTRefreshTokenRepository
from app.pkg import models
from app.pkg.models.exceptions.repository import EmptyResult


async def test_correct(
    refresh_token_repository: JWTRefreshTokenRepository,
    insert_first_refresh_token: models.JWTRefreshToken,
    second_refresh_token: str,
    second_fingerprint: str,
):
    command = models.UpdateJWTRefreshTokenCommand(
        user_id=insert_first_refresh_token.user_id,
        refresh_token=second_refresh_token,
        fingerprint=insert_first_refresh_token.fingerprint,
    )
    response = await refresh_token_repository.update(cmd=command)

    assert response == command


@pytest.mark.parametrize("iterable", [1, 2, 3, 4])
async def test_incorrect_user_id(
    refresh_token_repository: JWTRefreshTokenRepository,
    insert_first_refresh_token: models.JWTRefreshToken,
    second_refresh_token: str,
    second_fingerprint: str,
    iterable: int,
):
    command = models.UpdateJWTRefreshTokenCommand(
        user_id=insert_first_refresh_token.user_id + 1,
        refresh_token=second_refresh_token,
        fingerprint=insert_first_refresh_token.fingerprint,
    )

    with pytest.raises(EmptyResult):
        await refresh_token_repository.update(cmd=command)


@pytest.mark.parametrize(
    "fingerprint",
    [
        uuid.uuid4().__str__(),
        uuid.uuid4().__str__(),
        uuid.uuid4().__str__(),
    ],
)
async def test_incorrect_fingerprint_not_found(
    refresh_token_repository: JWTRefreshTokenRepository,
    insert_first_refresh_token: models.JWTRefreshToken,
    second_refresh_token: str,
    fingerprint: str,
):
    command = models.UpdateJWTRefreshTokenCommand(
        user_id=insert_first_refresh_token.user_id,
        refresh_token=second_refresh_token,
        fingerprint=fingerprint,
    )

    with pytest.raises(EmptyResult):
        await refresh_token_repository.update(cmd=command)
