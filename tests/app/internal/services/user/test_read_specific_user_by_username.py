import pytest

from app.internal.services import UserService
from app.pkg import models
from app.pkg.models.exceptions.repository import EmptyResult


async def test_correct(
    user_postgres_service: UserService,
    insert_first_user: models.User,
):
    result = await user_postgres_service.read_specific_user_by_username(
        query=models.ReadUserByUserNameQuery(username=insert_first_user.username)
    )
    assert result == insert_first_user


@pytest.mark.parametrize(
    "username",
    [
        "INCORRECT_USERNAME_1",
        "INCORRECT_USERNAME_2",
        "INCORRECT_USERNAME_3",
        "INCORRECT_USERNAME_4",
    ],
)
async def test_incorrect_username(user_postgres_service: UserService, username: str):
    with pytest.raises(EmptyResult):
        await user_postgres_service.read_specific_user_by_username(
            query=models.ReadUserByUserNameQuery(username=username)
        )
