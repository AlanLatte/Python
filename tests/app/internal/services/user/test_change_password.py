import uuid

import pytest
from pydantic import ValidationError

from app.internal.services import UserService
from app.pkg import models
from app.pkg.models.exceptions.repository import EmptyResult
from app.pkg.models.exceptions.user import IncorrectOldPassword


@pytest.mark.parametrize(
    "new_password",
    [
        uuid.uuid4().__str__(),
        uuid.uuid4().__str__(),
        uuid.uuid4().__str__(),
        uuid.uuid4().__str__(),
    ],
)
async def test_correct(
    user_postgres_service: UserService,
    insert_first_user: models.User,
    first_user: models.User,
    new_password: str,
):
    result = await user_postgres_service.change_password(
        cmd=models.ChangeUserPasswordCommand(
            id=insert_first_user.id,
            old_password=first_user.password.get_secret_value(),
            new_password=new_password.encode(),
        )
    )

    assert result == models.User(
        id=result.id,
        username=first_user.username,
        password=result.password,
        role_name=insert_first_user.role_name,
    )


async def test_incorrect_old_password(
    user_postgres_service: UserService,
    insert_first_user: models.User,
    first_user: models.User,
):

    with pytest.raises(IncorrectOldPassword):
        await user_postgres_service.change_password(
            cmd=models.ChangeUserPasswordCommand(
                id=insert_first_user.id,
                old_password="INCORRECT_OLD_PASSWORD",
                new_password="NEW_PASSWORD".encode(),
            )
        )


@pytest.mark.parametrize("user_id_offset", [1, 2, 3, 4])
async def test_incorrect_user_not_exist(
    user_postgres_service: UserService,
    insert_first_user: models.User,
    first_user: models.User,
    user_id_offset: int,
):
    with pytest.raises(EmptyResult):
        await user_postgres_service.change_password(
            cmd=models.ChangeUserPasswordCommand(
                id=insert_first_user.id + user_id_offset,
                old_password=first_user.password.get_secret_value(),
                new_password="NEW_PASSWORD".encode(),
            )
        )


@pytest.mark.parametrize(
    "new_password",
    ["1", "12", "123", "1234"],
)
async def test_incorrect_password_length(
    user_postgres_service: UserService,
    insert_first_user: models.User,
    first_user: models.User,
    new_password: str,
):
    with pytest.raises(ValidationError):
        await user_postgres_service.change_password(
            cmd=models.ChangeUserPasswordCommand(
                id=insert_first_user.id,
                old_password=first_user.password.get_secret_value(),
                new_password=new_password.encode(),
            )
        )
