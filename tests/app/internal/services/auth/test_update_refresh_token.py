import uuid

import pytest

from app.internal.services import AuthService
from app.pkg import models
from app.pkg.models.exceptions.repository import DriverError, EmptyResult


@pytest.mark.parametrize(
    "refresh_token",
    [
        uuid.uuid4().__str__(),
        uuid.uuid4().__str__(),
        uuid.uuid4().__str__(),
        uuid.uuid4().__str__(),
    ],
)
async def test_correct(
    auth_postgres_service: AuthService,
    insert_first_refresh_token: models.JWTRefreshToken,
    refresh_token: str,
):
    result = await auth_postgres_service.update_refresh_token(
        cmd=models.UpdateJWTRefreshTokenCommand(
            user_id=insert_first_refresh_token.user_id,
            refresh_token=refresh_token,
            fingerprint=insert_first_refresh_token.fingerprint,
        )
    )

    assert result != insert_first_refresh_token


@pytest.mark.parametrize(
    "refresh_token",
    [
        uuid.uuid4().__str__(),
        uuid.uuid4().__str__(),
        uuid.uuid4().__str__(),
        uuid.uuid4().__str__(),
    ],
)
async def test_incorrect_user_not_exists(
    auth_postgres_service: AuthService,
    insert_first_refresh_token: models.JWTRefreshToken,
    refresh_token: str,
):
    with pytest.raises(EmptyResult):
        await auth_postgres_service.update_refresh_token(
            cmd=models.UpdateJWTRefreshTokenCommand(
                user_id=insert_first_refresh_token.user_id + 1,
                refresh_token=refresh_token,
                fingerprint=insert_first_refresh_token.fingerprint,
            )
        )

