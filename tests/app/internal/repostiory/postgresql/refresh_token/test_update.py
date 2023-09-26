"""Test cases for :meth:`.JWTRefreshTokenRepository.update()`"""

import uuid

import pytest

from app.internal.repository.postgresql import JWTRefreshTokenRepository
from app.pkg import models
from app.pkg.models.exceptions.repository import EmptyResult


async def test_correct(
    refresh_token_repository: JWTRefreshTokenRepository,
    insert_first_refresh_token: models.JWTRefreshToken,
    create_model,
):
    cmd = await create_model(
        models.UpdateJWTRefreshTokenCommand,
        user_id=insert_first_refresh_token.user_id,
        fingerprint=insert_first_refresh_token.fingerprint,
    )
    response = await refresh_token_repository.update(cmd=cmd)

    assert response == cmd


@pytest.mark.repeat(10)
async def test_incorrect_user_id(
    refresh_token_repository: JWTRefreshTokenRepository,
    insert_first_refresh_token: models.JWTRefreshToken,
    create_model,
):
    cmd = await create_model(
        models.UpdateJWTRefreshTokenCommand,
        user_id=insert_first_refresh_token.user_id + 1,
        fingerprint=insert_first_refresh_token.fingerprint,
    )

    with pytest.raises(EmptyResult):
        await refresh_token_repository.update(cmd=cmd)


@pytest.mark.parametrize(
    "fingerprint",
    [
        uuid.uuid4(),
        uuid.uuid4(),
        uuid.uuid4(),
    ],
)
async def test_incorrect_fingerprint_not_found(
    refresh_token_repository: JWTRefreshTokenRepository,
    insert_first_refresh_token: models.JWTRefreshToken,
    create_model,
    fingerprint: uuid.UUID,
):
    cmd = await create_model(
        models.UpdateJWTRefreshTokenCommand,
        user_id=insert_first_refresh_token.user_id,
        fingerprint=str(fingerprint),
    )

    with pytest.raises(EmptyResult):
        await refresh_token_repository.update(cmd=cmd)
