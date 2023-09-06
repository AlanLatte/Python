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
    check_array_equality,
):
    users = await user_repository.read_all()
    assert check_array_equality(users, [insert_first_user, insert_second_user])


async def test_incorrect(user_repository: UserRepository):
    with pytest.raises(EmptyResult):
        await user_repository.read_all()


@pytest.mark.parametrize(
    "count",
    [1, 2, 3, 4],
)
async def test_correct_many_users(
    user_repository: UserRepository,
    create_model,
    count: int,
):
    with pytest.raises(EmptyResult):
        await user_repository.read_all()

    tasks = []
    for i in range(count):
        cmd = await create_model(
            models.CreateUserCommand,
            username=f"correct-{i}",
            password=f"strong-password-user-{i}",
        )
        feature = user_repository.create(cmd=cmd)
        tasks.append(feature)

    await asyncio.gather(*tasks)

    users = await user_repository.read_all()
    assert users.__len__() == count
