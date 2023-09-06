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
    create_model,
):
    with pytest.raises(DriverError):
        cmd = await create_model(
            models.CreateJWTRefreshTokenCommand,
            user_id=1,
        )
        await refresh_token_repository.create(cmd=cmd)


@pytest.mark.parametrize("count", [2, 3])
async def test_incorrect_unique_token(
    refresh_token_repository: JWTRefreshTokenRepository,
    insert_first_user: models.User,
    create_model,
    count: int,
):
    with pytest.raises(UniqueViolation):
        cmd = await create_model(
            models.CreateJWTRefreshTokenCommand,
            user_id=insert_first_user.id,
        )
        await refresh_token_repository.create(cmd=cmd)
        await refresh_token_repository.create(cmd=cmd)
