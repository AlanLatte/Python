import pytest

from app.internal.repository.postgresql.user import UserRepository
from app.pkg import models


@pytest.fixture()
async def insert_first_user(
    user_repository: UserRepository,
    first_user: models.User,
) -> models.User:

    first_user = first_user.migrate(models.User)
    first_user.password.crypt_password()
    return await user_repository.create(
        cmd=first_user.migrate(models.CreateUserCommand, random_fill=True),
    )


@pytest.fixture()
async def insert_second_user(
    user_repository: UserRepository,
    second_user: models.User,
) -> models.User:

    second_user = second_user.migrate(models.User)
    second_user.password.crypt_password()
    return await user_repository.create(
        cmd=second_user.migrate(models.CreateUserCommand, random_fill=True),
    )
