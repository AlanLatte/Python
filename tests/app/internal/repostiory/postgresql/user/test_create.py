import asyncio
import typing

import pytest
from pydantic import ValidationError

from app.internal.repository.postgresql.user import UserRepository
from app.pkg import models
from app.pkg.models.exceptions.repository import UniqueViolation


@pytest.mark.parametrize(
    "username",
    [
        "correct-1@example.ru",
        "correct-2@example.ru",
        "correct-3@example.ru",
        "correct-4@example.ru",
        "correct-5@example.ru",
        "correct-6@example.ru",
    ],
)
async def test_correct(user_repository: UserRepository, username: str, create_model):
    cmd = await create_model(models.CreateUserCommand, username=username)
    user = await user_repository.create(cmd=cmd)
    assert user.username == username


@pytest.mark.parametrize(
    "role",
    ["INCORRECT_ROLE", "SUPE_DUPER_MEGA_ADMIN_ROLE", "USER_1", "HELLO_WORLD"],
)
async def test_incorrect_user_role_name(
    user_repository: UserRepository, role: str, create_model
):
    with pytest.raises(expected_exception=ValidationError):
        cmd = await create_model(models.CreateUserCommand, role_name=role)
        await user_repository.create(cmd=cmd)


@pytest.mark.parametrize(
    "password",
    ["1", "12", "123", "1234", "12345"],
)
async def test_incorrect_password_length(
    user_repository: UserRepository, password: str, create_model
):
    with pytest.raises(expected_exception=ValidationError):
        cmd = await create_model(models.CreateUserCommand, password=password)
        await user_repository.create(cmd=cmd)


@pytest.mark.parametrize(
    "usernames",
    [
        ["correct-emaple-1@example.com"] * 2,
        ["correct-emaple-2@example.com"] * 2,
        ["correct-emaple-3@example.com"] * 2,
    ],
)
async def test_incorrect_already_exist(
    user_repository: UserRepository, usernames: typing.List[str], create_model
):
    with pytest.raises(expected_exception=UniqueViolation):
        tasks = []
        for i in usernames:

            feature = user_repository.create(
                cmd=await create_model(models.CreateUserCommand, username=i)
            )
            tasks.append(feature)

        await asyncio.gather(*tasks)
