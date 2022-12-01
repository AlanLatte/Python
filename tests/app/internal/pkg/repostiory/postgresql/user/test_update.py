import pytest
from pydantic import ValidationError

from app.internal.repository.postgresql import UserRepository
from app.pkg import models
from app.pkg.models.exceptions.repository import EmptyResult, UniqueViolation


@pytest.mark.parametrize(
    "username",
    [
        "updated-1@example.ru",
        "updated-2@example.ru",
        "updated-3@example.ru",
        "updated-4@example.ru",
        "updated-5@example.ru",
        "updated-6@example.ru",
    ],
)
async def test_correct_username(
    user_repository: UserRepository, insert_first_user: models.User, username: str,
):
    await user_repository.update(
        cmd=models.UpdateUserCommand(
            id=insert_first_user.id,
            username=username,
            password=insert_first_user.password.get_secret_value(),
        ),
    )

    user = await user_repository.read(
        query=models.ReadUserByIdQuery(id=insert_first_user.id),
    )

    insert_first_user.username = username

    assert user == insert_first_user


@pytest.mark.parametrize(
    "username",
    [
        "not_found-1@example.ru",
        "not_found-2@example.ru",
        "not_found-3@example.ru",
        "not_found-4@example.ru",
        "not_found-5@example.ru",
        "not_found-6@example.ru",
    ],
)
async def test_incorrect_unknown_user(
    user_repository: UserRepository, first_user: models.User, username: str,
):
    with pytest.raises(EmptyResult):
        first_user.username = username
        await user_repository.update(cmd=first_user.migrate(models.UpdateUserCommand))


async def test_already_exist(
    user_repository: UserRepository,
    insert_first_user: models.User,
    insert_second_user: models.User,
):
    with pytest.raises(UniqueViolation):
        insert_first_user.username = insert_second_user.username
        await user_repository.update(
            cmd=insert_first_user.migrate(models.UpdateUserCommand),
        )


@pytest.mark.parametrize(
    "user_role",
    ["INCORRECT_ROLE", "SUPE_DUPER_MEGA_ADMIN_ROLE", "USER_1", "HELLO_WORLD"],
)
async def test_incorrect_user_role(
    user_repository: UserRepository, insert_first_user: models.User, user_role: str,
):

    insert_first_user.role_name = user_role
    with pytest.raises(ValidationError):
        await user_repository.update(
            insert_first_user.migrate(models.UpdateUserCommand),
        )
