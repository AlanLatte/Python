import pytest

from app.internal.repository.postgresql.user_roles import UserRoleRepository
from app.pkg import models
from app.pkg.models.base import Model


async def test_correct_insert_models(
    user_role_repository: UserRoleRepository,
    create_model,
):
    for role in models.UserRole:
        cmd = await create_model(models.CreateUserRoleCommand, role_name=role.value)
        await user_role_repository.create(cmd=cmd)


async def test_correct(user_role_repository: UserRoleRepository):
    with pytest.raises(NotImplementedError):
        await user_role_repository.read(query=Model)
