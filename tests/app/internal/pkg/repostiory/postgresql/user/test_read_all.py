import asyncio

import pytest

from app.internal.repository.postgresql import UserRepository
from app.pkg import models
from app.pkg.models.exceptions.repository import EmptyResult


async def test_correct_one_users(
    user_repository: UserRepository,
    insert_first_user: models.User,
):
    users = await user_repository.read_all()
    assert insert_first_user in users


async def test_correct_two_users(
    user_repository: UserRepository,
    insert_first_user: models.User,
    insert_second_user: models.User,
):
    users = await user_repository.read_all()
    assert insert_first_user in users and insert_second_user in users


async def test_incorrect(user_repository: UserRepository):
    with pytest.raises(EmptyResult):
        await user_repository.read_all()


async def test_correct_many_users(user_repository: UserRepository):
    with pytest.raises(EmptyResult):
        await user_repository.read_all()

    tasks = []
    for i in range(10):
        feature = user_repository.create(
            models.CreateUserCommand(
                username=f"correct-{i}",
                password=f"strong-password-user-{i}",
                user_role=models.UserRole.USER,
            ),
        )
        tasks.append(feature)

    await asyncio.gather(*tasks)

    users = await user_repository.read_all()
    assert users.__len__() == 10
