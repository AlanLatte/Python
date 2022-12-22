import uuid

import pytest
from pydantic import ValidationError

from app.internal.services import UserService
from app.pkg import models
from app.pkg.models import UserRole
from app.pkg.models.exceptions.user import UserAlreadyExist
from app.pkg.models.types import NotEmptySecretStr


@pytest.mark.parametrize(
    "username,password",
    [
        [uuid.uuid4().__str__(), uuid.uuid4().__str__()],
        [uuid.uuid4().__str__(), uuid.uuid4().__str__()],
        [uuid.uuid4().__str__(), uuid.uuid4().__str__()],
    ],
)
async def test_correct(
    user_postgres_service: UserService, username: str, password: str
):
    result = await user_postgres_service.create_user(
        cmd=models.CreateUserCommand(
            username=username,
            password=password,
            role_name=UserRole.USER,
        )
    )
    secret_password = NotEmptySecretStr(password)

    assert result.password != secret_password

    assert result == models.User(
        id=result.id,
        username=username,
        password=result.password,
        role_name=UserRole.USER,
    )


@pytest.mark.parametrize(
    "username,password,role_name",
    [
        [uuid.uuid4().__str__(), uuid.uuid4().__str__(), "INCORRECT_USER_ROLE_1"],
        [uuid.uuid4().__str__(), uuid.uuid4().__str__(), "INCORRECT_USER_ROLE_2"],
        [uuid.uuid4().__str__(), uuid.uuid4().__str__(), "INCORRECT_USER_ROLE_3"],
    ],
)
async def test_incorrect_not_exists_user_role(
    user_postgres_service: UserService, username: str, password: str, role_name: str
):
    with pytest.raises(ValidationError):
        await user_postgres_service.create_user(
            cmd=models.CreateUserCommand(
                username=username,
                password=password,
                role_name=role_name,
            )
        )


@pytest.mark.parametrize(
    "username,password",
    [
        [uuid.uuid4().__str__(), "1"],
        [uuid.uuid4().__str__(), "12"],
        [uuid.uuid4().__str__(), "123"],
        [uuid.uuid4().__str__(), "1234"],
        [uuid.uuid4().__str__(), "12345"],
    ],
)
async def test_incorrect_password_length(
    user_postgres_service: UserService, username: str, password: str
):
    with pytest.raises(ValidationError):
        await user_postgres_service.create_user(
            cmd=models.CreateUserCommand(
                username=username,
                password=password,
                role_name=UserRole.USER,
            )
        )


async def test_incorrect_unique(
    user_postgres_service: UserService,
    insert_first_user: models.User,
    first_user: models.User,
):
    with pytest.raises(UserAlreadyExist):
        await user_postgres_service.create_user(
            cmd=models.CreateUserCommand(
                username=insert_first_user.username,
                password=first_user.password.get_secret_value(),
                role_name=insert_first_user.role_name,
            )
        )
