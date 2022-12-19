import psycopg2
import pytest

from app.internal.services import AuthService
from app.pkg import models
from app.pkg.models.exceptions.repository import DriverError, EmptyResult


async def test_correct_insert_one(
    auth_postgres_service: AuthService,
    insert_first_user: models.User,
    first_refresh_token: str,
    first_fingerprint: str,
    first_refresh_token_response: models.JWTRefreshToken,
):
    result = await auth_postgres_service.create_refresh_token(
        cmd=models.CreateJWTRefreshTokenCommand(
            user_id=insert_first_user.id,
            refresh_token=first_refresh_token,
            fingerprint=first_fingerprint,
        )
    )

    assert result == first_refresh_token_response


async def test_correct_insert_twice(
    auth_postgres_service: AuthService,
    insert_first_user: models.User,
    first_refresh_token: str,
    first_fingerprint: str,
    first_refresh_token_response: models.JWTRefreshToken,
    second_refresh_token: str,
    second_refresh_token_response: models.JWTRefreshToken,
):
    result = await auth_postgres_service.create_refresh_token(
        cmd=models.CreateJWTRefreshTokenCommand(
            user_id=insert_first_user.id,
            refresh_token=first_refresh_token,
            fingerprint=first_fingerprint,
        )
    )
    assert result == first_refresh_token_response

    result = await auth_postgres_service.create_refresh_token(
        cmd=models.CreateJWTRefreshTokenCommand(
            user_id=insert_first_user.id,
            refresh_token=second_refresh_token,
            fingerprint=first_fingerprint,
        )
    )

    assert result == models.JWTRefreshToken(
        user_id=insert_first_user.id,
        refresh_token=second_refresh_token,
        fingerprint=first_fingerprint,
    )


async def test_recreate_token(
    auth_postgres_service: AuthService,
    insert_first_user: models.User,
    first_refresh_token: str,
    first_fingerprint: str,
    second_refresh_token: str,
    first_refresh_token_response: models.JWTRefreshToken,
):
    await auth_postgres_service.create_refresh_token(
        cmd=models.CreateJWTRefreshTokenCommand(
            user_id=insert_first_user.id,
            refresh_token=first_refresh_token,
            fingerprint=first_fingerprint,
        )
    )

    # Testing recreate refresh token on UniqueViolation
    await auth_postgres_service.create_refresh_token(
        cmd=models.CreateJWTRefreshTokenCommand(
            user_id=insert_first_user.id,
            refresh_token=first_refresh_token,
            fingerprint=first_fingerprint,
        )
    )


@pytest.mark.parametrize("user_offset", [1, 2, 3, 4])
async def test_incorrect_not_exist_user(
    auth_postgres_service: AuthService,
    insert_first_user: models.User,
    first_refresh_token: str,
    first_fingerprint: str,
    user_offset: int,
):
    with pytest.raises(DriverError):
        await auth_postgres_service.create_refresh_token(
            cmd=models.CreateJWTRefreshTokenCommand(
                user_id=insert_first_user.id + user_offset,
                refresh_token=first_refresh_token,
                fingerprint=first_fingerprint,
            ),
        )
