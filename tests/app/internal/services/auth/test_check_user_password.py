import pytest
from pydantic import ValidationError

from app.internal.services.auth import AuthService
from app.pkg import models
from app.pkg.models.exceptions.auth import IncorrectUsernameOrPassword
from app.pkg.models.exceptions.repository import EmptyResult


async def test_correct(
    auth_postgres_service: AuthService,
    insert_first_user: models.User,
    first_user: models.User,
    create_model,
):
    cmd = await create_model(
        models.AuthCommand,
        username=first_user.username,
        password=first_user.password.get_secret_value(),
    )
    user = await auth_postgres_service.check_user_password(cmd=cmd)
    assert user == insert_first_user


@pytest.mark.repeat(5)
async def test_incorrect_password(
    auth_postgres_service: AuthService, insert_first_user: models.User, create_model
):
    with pytest.raises(IncorrectUsernameOrPassword):
        cmd = await create_model(
            models.AuthCommand,
            username=insert_first_user.username,
        )
        await auth_postgres_service.check_user_password(cmd=cmd)


@pytest.mark.repeat(10)
async def test_user_not_exist(
    auth_postgres_service: AuthService,
    insert_first_user: models.User,
    first_user: models.User,
    create_model,
):
    with pytest.raises(EmptyResult):
        cmd = await create_model(
            models.AuthCommand,
            password=first_user.password.get_secret_value(),
        )
        await auth_postgres_service.check_user_password(cmd=cmd)


@pytest.mark.parametrize(
    "fingerprint",
    [""],
)
async def test_small_length_fingerprint(
    auth_postgres_service: AuthService,
    insert_first_user: models.User,
    first_user: models.User,
    fingerprint: str,
    create_model,
):

    with pytest.raises(ValidationError):
        cmd = await create_model(
            models.AuthCommand,
            username=first_user.username,
            password=first_user.password.get_secret_value(),
            fingerprint=fingerprint,
        )
        await auth_postgres_service.check_user_password(cmd=cmd)
