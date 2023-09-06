import pytest

from app.internal.services import AuthService
from app.pkg import models
from app.pkg.models.exceptions.repository import EmptyResult


@pytest.mark.repeat(15)
async def test_correct(
    auth_postgres_service: AuthService,
    insert_first_refresh_token: models.JWTRefreshToken,
    create_model,
):
    cmd = await create_model(
        models.UpdateJWTRefreshTokenCommand,
        user_id=insert_first_refresh_token.user_id,
        fingerprint=insert_first_refresh_token.fingerprint,
    )
    result = await auth_postgres_service.update_refresh_token(cmd=cmd)

    assert result != insert_first_refresh_token


@pytest.mark.repeat(15)
async def test_incorrect_user_not_exists(
    auth_postgres_service: AuthService,
    insert_first_refresh_token: models.JWTRefreshToken,
    create_model,
):
    with pytest.raises(EmptyResult):
        cmd = await create_model(
            models.UpdateJWTRefreshTokenCommand,
            user_id=insert_first_refresh_token.user_id + 1,
            fingerprint=insert_first_refresh_token.fingerprint,
        )
        await auth_postgres_service.update_refresh_token(cmd=cmd)
