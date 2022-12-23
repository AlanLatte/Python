import pytest

from app.internal.repository.postgresql.refresh_tokens import JWTRefreshTokenRepository
from app.internal.services.auth import AuthService
from app.internal.services.user import UserService


@pytest.fixture()
async def auth_postgres_service(
    user_postgres_service: UserService,
    refresh_token_repository: JWTRefreshTokenRepository,
) -> AuthService:
    return AuthService(
        user_service=user_postgres_service,
        refresh_token_repository=refresh_token_repository,
    )
