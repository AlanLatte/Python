"""Tests cases for :meth:`.UserService.read_specific_user_by_id()`."""

import pytest

from app.internal.services import UserService
from app.pkg import models
from app.pkg.models.exceptions.repository import EmptyResult


async def test_correct(
    user_postgres_service: UserService,
    insert_first_user: models.User,
):
    result = await user_postgres_service.read_specific_user_by_id(
        query=models.ReadUserByIdQuery(id=insert_first_user.id),
    )

    assert result == insert_first_user


@pytest.mark.parametrize("user_id_offset", [1, 2, 3, 4])
async def test_incorrect_not_found(
    user_postgres_service: UserService,
    insert_first_user: models.User,
    user_id_offset: int,
):
    with pytest.raises(EmptyResult):
        await user_postgres_service.read_specific_user_by_id(
            query=models.ReadUserByIdQuery(id=insert_first_user.id + user_id_offset),
        )
