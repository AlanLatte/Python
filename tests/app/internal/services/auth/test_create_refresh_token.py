import pytest

from app.internal.services import AuthService
from app.pkg import models
from app.pkg.models.exceptions.repository import DriverError


async def test_correct_insert_one(
    auth_postgres_service: AuthService,
    insert_first_user: models.User,
    create_model,
):
    cmd = await create_model(
        models.CreateJWTRefreshTokenCommand,
        user_id=insert_first_user.id,
    )
    result = await auth_postgres_service.create_refresh_token(cmd=cmd)

    assert result == cmd


async def test_correct_insert_twice(
    auth_postgres_service: AuthService,
    insert_first_user: models.User,
    create_model,
):
    cmd = await create_model(
        models.CreateJWTRefreshTokenCommand,
        user_id=insert_first_user.id,
    )
    result = await auth_postgres_service.create_refresh_token(cmd=cmd)
    assert result == cmd

    cmd_second = await create_model(
        models.CreateJWTRefreshTokenCommand,
        user_id=insert_first_user.id,
        fingerprint=cmd.fingerprint,
    )

    result = await auth_postgres_service.create_refresh_token(cmd=cmd_second)

    assert result == await create_model(
        models.JWTRefreshToken,
        user_id=insert_first_user.id,
        refresh_token=result.refresh_token,
        fingerprint=cmd.fingerprint,
    )


async def test_recreate_token(
    auth_postgres_service: AuthService,
    insert_first_user: models.User,
    create_model,
):
    cmd = await create_model(
        models.CreateJWTRefreshTokenCommand,
        user_id=insert_first_user.id,
    )
    await auth_postgres_service.create_refresh_token(cmd=cmd)

    # Testing recreate refresh token on UniqueViolation
    await auth_postgres_service.create_refresh_token(cmd=cmd)


@pytest.mark.parametrize("user_offset", [1, 2, 3, 4])
async def test_incorrect_not_exist_user(
    auth_postgres_service: AuthService,
    insert_first_user: models.User,
    user_offset: int,
    create_model,
):
    with pytest.raises(DriverError):
        cmd = await create_model(
            models.CreateJWTRefreshTokenCommand,
            user_id=insert_first_user.id + user_offset,
        )
        await auth_postgres_service.create_refresh_token(cmd=cmd)
