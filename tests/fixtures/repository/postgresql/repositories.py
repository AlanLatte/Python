import pytest
from app.internal.repository.postgresql.user import UserRepository


@pytest.fixture()
def user_repository() -> UserRepository:
    return UserRepository()
