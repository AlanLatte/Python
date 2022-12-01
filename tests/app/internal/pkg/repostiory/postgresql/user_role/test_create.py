import pytest

from app.pkg import models
from app.pkg.models.base import Model
from app.pkg.models.exceptions.repository import EmptyResult
from app.internal.repository.postgresql.user_roles import UserRoleRepository


async def test_correct_insert_models(user_role_repository: UserRoleRepository):
    with pytest.raises(EmptyResult):
        for role in models.UserRole:
            await user_role_repository.create(
                cmd=models.CreateUserRoleCommand(role_name=role.value)
            )


async def test_correct(user_role_repository: UserRoleRepository):
    with pytest.raises(NotImplementedError):
        await user_role_repository.read(query=Model)
