"""Test cases for :meth:`.UserService.create_user()`."""

import pytest

from app.internal.repository.postgresql import connection
from app.internal.services import UserService
from app.internal.services.user_roles import UserRoleService
from app.pkg import models
from app.pkg.models.base import BaseAPIException
from app.pkg.models.exceptions.repository import DriverError


async def test_correct(
    user_role_postgres_service: UserRoleService,
    user_postgres_service: UserService,
    first_user: models.User,
):
    q = """
        truncate table user_roles cascade;
    """

    async with connection.get_connection() as cursor:
        await cursor.execute(q)

    with pytest.raises(DriverError):
        await user_postgres_service.create_user(
            cmd=first_user.migrate(model=models.CreateUserCommand),
        )

    async for i in user_role_postgres_service.create_all_user_roles():
        assert not isinstance(i, BaseAPIException)

    result = await user_postgres_service.create_user(
        cmd=first_user.migrate(model=models.CreateUserCommand),
    )

    assert result == await user_postgres_service.read_specific_user_by_id(
        query=models.ReadUserByIdQuery(id=result.id),
    )


async def test_exists_user_roles(
    user_role_postgres_service: UserRoleService,
):
    async for i in user_role_postgres_service.create_all_user_roles():
        assert i is None
