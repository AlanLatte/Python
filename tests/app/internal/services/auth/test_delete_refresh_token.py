import uuid

import pytest

from app.internal.services import AuthService
from app.pkg import models
from app.pkg.models.exceptions.jwt import UnAuthorized
from app.pkg.models.types import NotEmptySecretStr


async def test_correct(
    auth_postgres_service: AuthService,
    insert_first_refresh_token: models.JWTRefreshToken,
):
    result = await auth_postgres_service.delete_refresh_token(
        cmd=insert_first_refresh_token.migrate(models.DeleteJWTRefreshTokenCommand)
    )
    assert result == insert_first_refresh_token

    result = await auth_postgres_service.check_user_exist_refresh_token(
        query=models.ReadJWTRefreshTokenQueryByFingerprint(
            user_id=insert_first_refresh_token.user_id,
            fingerprint=insert_first_refresh_token.fingerprint,
        )
    )
    assert not result


@pytest.mark.parametrize("user_id_offset", [1, 2, 3, 4, 5])
async def test_incorrect_user_not_exists(
    auth_postgres_service: AuthService,
    insert_first_refresh_token: models.JWTRefreshToken,
    user_id_offset: int,
):
    insert_first_refresh_token = insert_first_refresh_token.copy()

    insert_first_refresh_token.user_id += user_id_offset
    with pytest.raises(UnAuthorized):
        await auth_postgres_service.delete_refresh_token(
            cmd=insert_first_refresh_token.migrate(models.DeleteJWTRefreshTokenCommand)
        )


@pytest.mark.parametrize(
    "fingerprint",
    [
        uuid.uuid4().__str__(),
        uuid.uuid4().__str__(),
        uuid.uuid4().__str__(),
        uuid.uuid4().__str__(),
    ],
)
async def test_incorrect_user_fingerprint_not_exists(
    auth_postgres_service: AuthService,
    insert_first_refresh_token: models.JWTRefreshToken,
    fingerprint: str,
):
    insert_first_refresh_token = insert_first_refresh_token.copy()

    insert_first_refresh_token.fingerprint = NotEmptySecretStr(fingerprint)
    with pytest.raises(UnAuthorized):
        await auth_postgres_service.delete_refresh_token(
            cmd=insert_first_refresh_token.migrate(models.DeleteJWTRefreshTokenCommand)
        )
