import uuid

import pytest

from app.internal.repository.postgresql import JWTRefreshTokenRepository
from app.pkg import models
from app.pkg.models.exceptions.repository import EmptyResult


async def test_correct(
    refresh_token_repository: JWTRefreshTokenRepository,
    insert_first_refresh_token: models.JWTRefreshToken,
):

    response = await refresh_token_repository.read_by_fingerprint(
        query=models.ReadJWTRefreshTokenQueryByFingerprint(
            user_id=insert_first_refresh_token.user_id,
            fingerprint=insert_first_refresh_token.fingerprint,
        ),
    )
    assert response == insert_first_refresh_token


@pytest.mark.parametrize(
    "fingerprint",
    [
        uuid.uuid4().__str__(),
        uuid.uuid4().__str__(),
        uuid.uuid4().__str__(),
    ],
)
async def test_incorrect_empty_result(
    refresh_token_repository: JWTRefreshTokenRepository,
    insert_first_refresh_token: models.JWTRefreshToken,
    fingerprint: str,
):
    with pytest.raises(EmptyResult):
        await refresh_token_repository.read_by_fingerprint(
            query=models.ReadJWTRefreshTokenQueryByFingerprint(
                user_id=insert_first_refresh_token.user_id,
                fingerprint=fingerprint,
            ),
        )
