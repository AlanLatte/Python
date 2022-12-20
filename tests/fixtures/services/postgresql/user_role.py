import pytest

from app.internal.services.user_roles import UserRoleService
from app.internal.repository.postgresql.user_roles import UserRoleRepository


@pytest.fixture()
async def user_role_postgres_service(
    user_role_repository: UserRoleRepository,
) -> UserRoleService:
    return UserRoleService(user_role_repository=user_role_repository)
