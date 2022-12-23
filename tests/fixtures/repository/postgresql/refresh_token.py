from uuid import uuid4

import pytest

from app.internal.repository.postgresql import JWTRefreshTokenRepository
from app.pkg import models
from app.pkg.models import CreateJWTRefreshTokenCommand, JWTRefreshToken


@pytest.fixture
def first_refresh_token():
    return uuid4().__str__()


@pytest.fixture
def second_refresh_token():
    return uuid4().__str__()


@pytest.fixture
def first_fingerprint():
    return uuid4().__str__()


@pytest.fixture
def second_fingerprint():
    return uuid4().__str__()


@pytest.fixture
def first_refresh_token_response(
    insert_first_user: models.User,
    first_refresh_token: models.JWTRefreshToken,
    first_fingerprint: str,
):
    return JWTRefreshToken(
        user_id=insert_first_user.id,
        refresh_token=first_refresh_token,
        fingerprint=first_fingerprint,
    )


@pytest.fixture
def second_refresh_token_response(
    insert_second_user: models.User,
    second_refresh_token: models.JWTRefreshToken,
    second_fingerprint: str,
):
    return JWTRefreshToken(
        user_id=insert_second_user.id,
        refresh_token=second_refresh_token,
        fingerprint=second_fingerprint,
    )


@pytest.fixture
async def insert_first_refresh_token(
    insert_first_user: models.User,
    refresh_token_repository: JWTRefreshTokenRepository,
    first_refresh_token: models.JWTRefreshToken,
    first_fingerprint: str,
):
    return await refresh_token_repository.create(
        cmd=CreateJWTRefreshTokenCommand(
            user_id=insert_first_user.id,
            refresh_token=first_refresh_token,
            fingerprint=first_fingerprint,
        ),
    )


@pytest.fixture
async def insert_second_refresh_token(
    insert_second_user: models.User,
    refresh_token_repository: JWTRefreshTokenRepository,
    second_refresh_token: models.JWTRefreshToken,
    second_fingerprint: str,
):
    return await refresh_token_repository.create(
        cmd=CreateJWTRefreshTokenCommand(
            user_id=insert_second_user.id,
            refresh_token=second_refresh_token,
            fingerprint=second_fingerprint,
        ),
    )
