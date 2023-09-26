"""Tests cases for :meth:`.UserService.delete_specific_user()`."""

import pytest

from app.internal.services import UserService
from app.pkg import models
from app.pkg.models.exceptions.repository import EmptyResult


async def test_correct(
    user_postgres_service: UserService,
    insert_first_user: models.User,
):
    result = await user_postgres_service.delete_specific_user(
        cmd=models.DeleteUserCommand(id=insert_first_user.id),
    )

    with pytest.raises(EmptyResult):
        await user_postgres_service.read_specific_user_by_id(
            query=models.ReadUserByIdQuery(id=result.id),
        )


async def test_not_found_user(
    user_postgres_service: UserService,
    first_user: models.User,
):
    with pytest.raises(EmptyResult):
        await user_postgres_service.delete_specific_user(
            cmd=models.DeleteUserCommand(id=first_user.id),
        )


async def test_correct_delete_one_of_two_users(
    user_postgres_service: UserService,
    insert_first_user: models.User,
    insert_second_user: models.User,
):
    result = await user_postgres_service.delete_specific_user(
        cmd=models.DeleteUserCommand(id=insert_first_user.id),
    )

    with pytest.raises(EmptyResult):
        await user_postgres_service.read_specific_user_by_id(
            query=models.ReadUserByIdQuery(id=result.id),
        )

    assert insert_second_user == await user_postgres_service.read_specific_user_by_id(
        query=models.ReadUserByIdQuery(id=insert_second_user.id),
    )
