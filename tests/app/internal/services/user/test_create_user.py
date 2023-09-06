import uuid

import pytest
from pydantic import ValidationError

from app.internal.services import UserService
from app.pkg import models
from app.pkg.models.exceptions.user import UserAlreadyExist
from app.pkg.models.types import EncryptedSecretBytes


@pytest.mark.repeat(10)
async def test_correct(user_postgres_service: UserService, create_model):
    cmd = await create_model(
        models.CreateUserCommand,
    )
    result = await user_postgres_service.create_user(cmd=cmd)

    secret_password = EncryptedSecretBytes(cmd.password.get_secret_value())

    assert result.password != secret_password

    assert result == await create_model(
        models.User,
        id=result.id,
        username=cmd.username,
        password=secret_password.get_secret_value(),
        role_name=cmd.role_name,
    )


@pytest.mark.repeat(5)
async def test_incorrect_not_exists_user_role(
    user_postgres_service: UserService,
    create_model,
):
    with pytest.raises(ValidationError):
        cmd = await create_model(
            models.CreateUserCommand,
            role_name=uuid.uuid4().__str__(),
        )
        await user_postgres_service.create_user(cmd=cmd)


@pytest.mark.parametrize(
    "password",
    ["1", "12", "123", "1234", "12345"],
)
async def test_incorrect_password_length(
    user_postgres_service: UserService,
    password: str,
    create_model,
):
    with pytest.raises(ValidationError):
        cmd = await create_model(
            models.CreateUserCommand,
            password=password,
        )
        await user_postgres_service.create_user(cmd=cmd)


async def test_incorrect_unique(
    user_postgres_service: UserService,
    insert_first_user: models.User,
    first_user: models.User,
    create_model,
):
    cmd = await create_model(
        models.CreateUserCommand,
        username=insert_first_user.username,
    )
    with pytest.raises(UserAlreadyExist):
        await user_postgres_service.create_user(cmd=cmd)
