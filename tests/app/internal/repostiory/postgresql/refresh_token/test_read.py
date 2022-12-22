import uuid

import pytest

from app.internal.repository.postgresql import JWTRefreshTokenRepository
from app.pkg import models
from app.pkg.models.exceptions.repository import EmptyResult


async def test_correct(
    refresh_token_repository: JWTRefreshTokenRepository,
    insert_first_user: models.User,
    insert_first_refresh_token: models.JWTRefreshToken,
):
    response = await refresh_token_repository.read(
        query=models.ReadJWTRefreshTokenQuery(
            user_id=insert_first_user.id,
            refresh_token=insert_first_refresh_token.refresh_token.get_secret_value(),
        )
    )

    assert response == insert_first_refresh_token


@pytest.mark.parametrize(
    "refresh_token",
    [
        uuid.uuid4().__str__(),
        uuid.uuid4().__str__(),
        uuid.uuid4().__str__(),
    ],
)
async def test_empty_result(
    refresh_token_repository: JWTRefreshTokenRepository,
    insert_first_user: models.User,
    refresh_token: str,
):
    with pytest.raises(EmptyResult):
        await refresh_token_repository.read(
            query=models.ReadJWTRefreshTokenQuery(
                user_id=insert_first_user.id,
                refresh_token=refresh_token,
            )
        )
