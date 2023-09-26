"""Tests cases for :meth:`.UserService.change_password()`."""

import pytest
from pydantic import ValidationError

from app.internal.services import UserService
from app.pkg import models
from app.pkg.models.exceptions.repository import EmptyResult
from app.pkg.models.exceptions.user import IncorrectOldPassword


@pytest.mark.repeat(10)
async def test_correct(
    user_postgres_service: UserService,
    insert_first_user: models.User,
    first_user: models.User,
    create_model,
):
    cmd = await create_model(
        models.ChangeUserPasswordCommand,
        id=insert_first_user.id,
        old_password=first_user.password.get_secret_value(),
    )
    result = await user_postgres_service.change_password(cmd=cmd)

    assert result.password != insert_first_user.password


@pytest.mark.repeat(10)
async def test_incorrect_old_password(
    user_postgres_service: UserService,
    insert_first_user: models.User,
    create_model,
):
    cmd = await create_model(models.ChangeUserPasswordCommand, id=insert_first_user.id)
    with pytest.raises(IncorrectOldPassword):
        await user_postgres_service.change_password(cmd=cmd)


@pytest.mark.parametrize("user_id_offset", [1, 2, 3, 4])
async def test_incorrect_user_not_exist(
    user_postgres_service: UserService,
    insert_first_user: models.User,
    first_user: models.User,
    user_id_offset: int,
    create_model,
):
    cmd = await create_model(
        models.ChangeUserPasswordCommand,
        id=insert_first_user.id + user_id_offset,
        old_password=first_user.password.get_secret_value(),
    )
    with pytest.raises(EmptyResult):
        await user_postgres_service.change_password(cmd=cmd)


@pytest.mark.parametrize(
    "new_password",
    ["1", "12", "123", "1234"],
)
async def test_incorrect_password_length(
    user_postgres_service: UserService,
    insert_first_user: models.User,
    first_user: models.User,
    new_password: str,
    create_model,
):
    with pytest.raises(ValidationError):
        cmd = await create_model(
            models.ChangeUserPasswordCommand,
            id=insert_first_user.id,
            old_password=first_user.password.get_secret_value(),
            new_password=new_password.encode(),
        )
        await user_postgres_service.change_password(cmd=cmd)
