import pytest

from app.internal.repository.postgresql.user import UserRepository
from app.internal.services.user import UserService


@pytest.fixture()
async def user_postgres_service(user_repository: UserRepository) -> UserService:
    return UserService(user_repository=user_repository)
