"""Test cases for :meth:`.UserService.read_specific_user_by_username()`."""

import pytest

from app.internal.services import UserService
from app.pkg import models
from app.pkg.models.exceptions.repository import EmptyResult


async def test_correct(
    user_postgres_service: UserService,
    insert_first_user: models.User,
):
    result = await user_postgres_service.read_specific_user_by_username(
        query=models.ReadUserByUserNameQuery(username=insert_first_user.username),
    )

    assert result == insert_first_user


@pytest.mark.repeat(10)
async def test_incorrect_username(user_postgres_service: UserService, create_model):
    with pytest.raises(EmptyResult):
        query = await create_model(models.ReadUserByUserNameQuery)

        await user_postgres_service.read_specific_user_by_username(query=query)
