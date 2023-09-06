import pytest

from app.internal.repository.postgresql.refresh_tokens import JWTRefreshTokenRepository
from app.pkg import models
from app.pkg.models.exceptions.repository import DriverError, EmptyResult


async def test_correct(
    refresh_token_repository: JWTRefreshTokenRepository,
    insert_first_refresh_token: models.JWTRefreshToken,
    insert_first_user: models.User,
    create_model,
):
    cmd = await create_model(
        models.DeleteJWTRefreshTokenCommand,
        user_id=insert_first_user.id,
        fingerprint=insert_first_refresh_token.fingerprint,
        refresh_token=insert_first_refresh_token.refresh_token,
    )
    response = await refresh_token_repository.delete(cmd=cmd)

    assert response == cmd.migrate(models.JWTRefreshToken)


@pytest.mark.parametrize(
    "user_id",
    [1, 2, 3, 4],
)
async def test_user_does_exist(
    refresh_token_repository: JWTRefreshTokenRepository,
    user_id: int,
    create_model,
):
    cmd = await create_model(
        models.DeleteJWTRefreshTokenCommand,
        user_id=user_id,
    )
    with pytest.raises(DriverError):
        await refresh_token_repository.create(cmd=cmd)


@pytest.mark.repeat(10)
async def test_not_exist(
    refresh_token_repository: JWTRefreshTokenRepository,
    insert_first_user: models.User,
    create_model,
):
    cmd = await create_model(
        models.DeleteJWTRefreshTokenCommand,
        user_id=insert_first_user.id,
    )
    with pytest.raises(EmptyResult):
        await refresh_token_repository.delete(cmd=cmd)
