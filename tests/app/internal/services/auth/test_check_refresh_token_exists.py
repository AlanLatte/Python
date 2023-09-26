"""Test cases for :meth:`.AuthService.check_refresh_token_exists()`."""

import pytest

from app.internal.services import AuthService
from app.pkg import models
from app.pkg.models.exceptions.jwt import UnAuthorized


async def test_correct(
    insert_first_refresh_token: models.JWTRefreshToken,
    auth_postgres_service: AuthService,
):
    response = await auth_postgres_service.check_refresh_token_exists(
        query=models.ReadJWTRefreshTokenQuery(
            user_id=insert_first_refresh_token.user_id,
            refresh_token=insert_first_refresh_token.refresh_token,
        ),
    )
    assert response == insert_first_refresh_token


@pytest.mark.parametrize("user_offset", [1, 2, 3, 4, 5])
async def test_incorrect_user_not_exist(
    auth_postgres_service: AuthService,
    insert_first_user: models.User,
    user_offset: int,
    create_model,
):
    with pytest.raises(UnAuthorized):
        query = await create_model(
            models.ReadJWTRefreshTokenQuery,
            user_id=insert_first_user.id + user_offset,
        )
        await auth_postgres_service.check_refresh_token_exists(query=query)


@pytest.mark.repeat(5)
async def test_incorrect_token_not_exist(
    auth_postgres_service: AuthService,
    insert_first_user: models.User,
    create_model,
):
    with pytest.raises(UnAuthorized):
        query = await create_model(
            models.ReadJWTRefreshTokenQuery,
            user_id=insert_first_user.id,
        )
        await auth_postgres_service.check_refresh_token_exists(query=query)
