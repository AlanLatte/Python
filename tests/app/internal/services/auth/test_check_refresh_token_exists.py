import uuid

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
    first_refresh_token: str,
    insert_first_user: models.User,
    user_offset: int,
):
    with pytest.raises(UnAuthorized):
        await auth_postgres_service.check_refresh_token_exists(
            query=models.ReadJWTRefreshTokenQuery(
                user_id=insert_first_user.id + user_offset,
                refresh_token=first_refresh_token,
            ),
        )


@pytest.mark.parametrize(
    "refresh_token",
    [
        uuid.uuid4().__str__(),
        uuid.uuid4().__str__(),
        uuid.uuid4().__str__(),
        uuid.uuid4().__str__(),
    ],
)
async def test_incorrect_token_not_exist(
    auth_postgres_service: AuthService,
    refresh_token: str,
    insert_first_user: models.User,
):
    with pytest.raises(UnAuthorized):
        await auth_postgres_service.check_refresh_token_exists(
            query=models.ReadJWTRefreshTokenQuery(
                user_id=insert_first_user.id,
                refresh_token=refresh_token,
            ),
        )
