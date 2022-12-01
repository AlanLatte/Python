import asyncio

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
async def test_correct(user_repository: UserRepository, username):
    cmd = models.CreateUserCommand(
        username=username,
        password="supeR_%$tr0ng-pa$$worD",
        role_name=models.UserRole.USER,
    )
    user = await user_repository.create(cmd=cmd)
    assert user.username == username


@pytest.mark.parametrize(
    "role",
    ["INCORRECT_ROLE", "SUPE_DUPER_MEGA_ADMIN_ROLE", "USER_1", "HELLO_WORLD"],
)
async def test_incorrect_user_role_name(user_repository: UserRepository, role: str):
    with pytest.raises(expected_exception=ValidationError):
        cmd = models.CreateUserCommand(
            username="correct-email@example.ru",
            password="supeR_%$tr0ng-pa$$worD",
            role_name=role,
        )
        await user_repository.create(cmd=cmd)


@pytest.mark.parametrize(
    "password",
    ["1", "12", "123", "1234", "12345"],
)
async def test_incorrect_password_length(
    user_repository: UserRepository, password: str
):
    with pytest.raises(expected_exception=ValidationError):
        await user_repository.create(
            cmd=models.CreateUserCommand(
                username="correct-1@example.ru",
                password=password,
                role_name=models.UserRole.USER,
            )
        )


async def test_incorrect_already_exist(user_repository: UserRepository):
    with pytest.raises(expected_exception=UniqueViolation):
        tasks = []
        for i in range(2):
            feature = user_repository.create(
                cmd=models.CreateUserCommand(
                    username="correct-email@example.ru",
                    password="supeR_%$tr0ng-pa$$worD",
                    role_name=models.UserRole.USER,
                )
            )
            tasks.append(feature)

        await asyncio.gather(*tasks)
