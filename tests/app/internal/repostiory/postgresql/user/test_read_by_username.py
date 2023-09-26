"""Test cases for :meth:`.UserRepository.read_by_username()`."""

import pytest

from app.internal.repository.postgresql import UserRepository
from app.pkg import models
from app.pkg.models.exceptions.repository import EmptyResult


async def test_correct(user_repository: UserRepository, insert_first_user: models.User):
    user = await user_repository.read_by_username(
        query=models.ReadUserByUserNameQuery(username=insert_first_user.username),
    )
    assert user == insert_first_user


@pytest.mark.parametrize(
    "username",
    [
        "incorrect-1@example.ru",
        "incorrect-2@example.ru",
        "incorrect-3@example.ru",
        "incorrect-4@example.ru",
        "incorrect-5@example.ru",
        "incorrect-6@example.ru",
    ],
)
async def test_incorrect(user_repository: UserRepository, username: str):
    with pytest.raises(EmptyResult):
        await user_repository.read_by_username(
            query=models.ReadUserByUserNameQuery(username=username),
        )
