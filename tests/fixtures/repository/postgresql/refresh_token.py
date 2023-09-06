import pytest

from app.internal.repository.postgresql import JWTRefreshTokenRepository
from app.pkg import models


@pytest.fixture
def first_refresh_token_response(
    insert_first_user: models.User,
):
    return insert_first_user.migrate(
        models.JWTRefreshToken,
        random_fill=True,
        match_keys={"user_id": "id"},
    )


@pytest.fixture
def second_refresh_token_response(
    insert_second_user: models.User,
):
    return insert_second_user.migrate(
        models.JWTRefreshToken,
        random_fill=True,
        match_keys={"user_id": "id"},
    )


@pytest.fixture
async def insert_first_refresh_token(
    insert_first_user: models.User,
    refresh_token_repository: JWTRefreshTokenRepository,
):
    return await refresh_token_repository.create(
        cmd=insert_first_user.migrate(
            models.CreateJWTRefreshTokenCommand,
            random_fill=True,
            match_keys={"user_id": "id"},
        ),
    )


@pytest.fixture
async def insert_second_refresh_token(
    insert_second_user: models.User,
    refresh_token_repository: JWTRefreshTokenRepository,
):
    return await refresh_token_repository.create(
        cmd=insert_second_user.migrate(
            models.CreateJWTRefreshTokenCommand,
            random_fill=True,
            match_keys={"user_id": "id"},
        ),
    )
