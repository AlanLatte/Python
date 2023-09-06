import pytest

from app.internal.services import UserService
from app.pkg import models
from app.pkg.models.exceptions.repository import EmptyResult


async def test_correct(
    user_postgres_service: UserService,
    insert_first_user: models.User,
    insert_second_user: models.User,
    check_array_equality,
):
    result = await user_postgres_service.read_all_users()
    assert check_array_equality(result, [insert_first_user, insert_second_user])


async def test_empty_result(user_postgres_service: UserService):
    with pytest.raises(EmptyResult):
        await user_postgres_service.read_all_users()
