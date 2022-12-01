import pytest

from app.internal.repository.postgresql.user import UserRepository
from app.internal.repository.postgresql.user_roles import UserRoleRepository


@pytest.fixture()
def user_repository() -> UserRepository:
    return UserRepository()


@pytest.fixture()
def user_role_repository() -> UserRepository:
    return UserRoleRepository()
