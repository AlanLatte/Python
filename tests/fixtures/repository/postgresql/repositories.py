import pytest

from app.internal.repository.postgresql import JWTRefreshTokenRepository
from app.internal.repository.postgresql.user import UserRepository
from app.internal.repository.postgresql.user_roles import UserRoleRepository


@pytest.fixture()
async def user_repository() -> UserRepository:
    return UserRepository()


@pytest.fixture()
async def user_role_repository() -> UserRoleRepository:
    return UserRoleRepository()


@pytest.fixture()
async def refresh_token_repository() -> JWTRefreshTokenRepository:
    return JWTRefreshTokenRepository()
