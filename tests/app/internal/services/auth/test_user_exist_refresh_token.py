"""Test cases for :meth:`.AuthService.create_refresh_token()`."""

import pytest

from app.internal.services.auth import AuthService
from app.pkg import models


async def test_correct(
    auth_postgres_service: AuthService,
    insert_first_refresh_token: models.JWTRefreshToken,
    create_model,
):
    query = await create_model(
        models.ReadJWTRefreshTokenQueryByFingerprint,
        user_id=insert_first_refresh_token.user_id,
        fingerprint=insert_first_refresh_token.fingerprint,
    )
    result = await auth_postgres_service.check_user_exist_refresh_token(query=query)
    assert result == insert_first_refresh_token


@pytest.mark.repeat(15)
async def test_not_exist_token(auth_postgres_service: AuthService, create_model):
    query = await create_model(
        models.ReadJWTRefreshTokenQueryByFingerprint,
    )
    result = await auth_postgres_service.check_user_exist_refresh_token(query=query)

    assert not result
