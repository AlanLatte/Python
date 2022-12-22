import uuid

import pytest

from app.internal.services.auth import AuthService
from app.pkg import models
from app.pkg.models.exceptions.jwt import UnAuthorized


async def test_correct(
    auth_postgres_service: AuthService,
    first_user: models.User,
    insert_first_refresh_token: models.JWTRefreshToken,
    first_fingerprint: str,
):
    result = await auth_postgres_service.check_user_exist_refresh_token(
        query=models.ReadJWTRefreshTokenQueryByFingerprint(
            user_id=insert_first_refresh_token.user_id,
            fingerprint=insert_first_refresh_token.fingerprint,
        )
    )
    assert result == insert_first_refresh_token


@pytest.mark.parametrize(
    "user_id,fingerprint",
    [
        [1, uuid.uuid4().__str__()],
        [2, uuid.uuid4().__str__()],
        [3, uuid.uuid4().__str__()],
        [4, uuid.uuid4().__str__()],
    ],
)
async def test_not_exist_token(
    auth_postgres_service: AuthService,
    user_id: int,
    fingerprint: str,
):
    result = await auth_postgres_service.check_user_exist_refresh_token(
        query=models.ReadJWTRefreshTokenQueryByFingerprint(
            user_id=user_id,
            fingerprint=fingerprint,
        )
    )

    assert not result
