import uuid

import pytest

from app.internal.repository.postgresql import JWTRefreshTokenRepository
from app.pkg import models
from app.pkg.models.exceptions.repository import DriverError, UniqueViolation


@pytest.mark.parametrize(
    "refresh_token_value,fingerprint_value",
    [
        (uuid.uuid4().__str__(), uuid.uuid4().__str__()),
        (uuid.uuid4().__str__(), uuid.uuid4().__str__()),
        (uuid.uuid4().__str__(), uuid.uuid4().__str__()),
    ],
)
async def test_correct(
    refresh_token_repository: JWTRefreshTokenRepository,
    insert_first_user: models.User,
    refresh_token_value: str,
    fingerprint_value: str,
):
    refresh_token: models.JWTRefreshToken = await refresh_token_repository.create(
        cmd=models.CreateJWTRefreshTokenCommand(
            user_id=insert_first_user.id,
            fingerprint=uuid.uuid4().__str__(),
            refresh_token=refresh_token_value,
        ),
    )
    wait_for_response = models.JWTRefreshToken(
        user_id=insert_first_user.id,
        refresh_token=refresh_token_value,
        fingerprint=fingerprint_value,
    )
    assert refresh_token.refresh_token == wait_for_response.refresh_token


async def test_incorrect_empty_user(
    refresh_token_repository: JWTRefreshTokenRepository,
    first_fingerprint: str,
    first_refresh_token: str,
):
    with pytest.raises(DriverError):
        await refresh_token_repository.create(
            cmd=models.CreateJWTRefreshTokenCommand(
                user_id=1,
                fingerprint=uuid.uuid4().__str__(),
                refresh_token=first_refresh_token,
            ),
        )


async def test_incorrect_unique_token(
    refresh_token_repository: JWTRefreshTokenRepository,
    insert_first_user: models.User,
    first_fingerprint: str,
    first_refresh_token: str,
):
    with pytest.raises(UniqueViolation):
        for _ in range(3):
            await refresh_token_repository.create(
                cmd=models.CreateJWTRefreshTokenCommand(
                    user_id=insert_first_user.id,
                    fingerprint=first_fingerprint,
                    refresh_token=first_refresh_token,
                ),
            )
            await refresh_token_repository.create(
                cmd=models.CreateJWTRefreshTokenCommand(
                    user_id=insert_first_user.id,
                    fingerprint=first_fingerprint,
                    refresh_token=first_refresh_token,
                ),
            )
