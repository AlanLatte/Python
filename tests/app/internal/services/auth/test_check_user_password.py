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
    first_fingerprint: str,
):

    user = await auth_postgres_service.check_user_password(
        cmd=models.AuthCommand(
            username=first_user.username,
            password=first_user.password.get_secret_value(),
            fingerprint=first_fingerprint,
        ),
    )
    assert user == insert_first_user


@pytest.mark.parametrize(
    "password",
    [
        b"FAKE_PASSWORD_0",
        b"FAKE_PASSWORD_1",
        b"FAKE_PASSWORD_2",
        b"FAKE_PASSWORD_3",
    ],
)
async def test_incorrect_password(
    auth_postgres_service: AuthService,
    insert_first_user: models.User,
    first_fingerprint: str,
    password: bytes,
):
    with pytest.raises(IncorrectUsernameOrPassword):
        await auth_postgres_service.check_user_password(
            cmd=models.AuthCommand(
                username=insert_first_user.username,
                password=password,
                fingerprint=first_fingerprint,
            ),
        )


@pytest.mark.parametrize(
    "username",
    [
        "FAKE_USERNAME_1",
        "FAKE_USERNAME_2",
        "FAKE_USERNAME_3",
        "FAKE_USERNAME_4",
    ],
)
async def test_user_not_exist(
    auth_postgres_service: AuthService,
    insert_first_user: models.User,
    first_user: models.User,
    first_fingerprint: str,
    username: str,
):
    with pytest.raises(EmptyResult):
        await auth_postgres_service.check_user_password(
            cmd=models.AuthCommand(
                username=username,
                password=first_user.password.get_secret_value(),
                fingerprint=first_fingerprint,
            ),
        )


@pytest.mark.parametrize(
    "fingerprint",
    [""],
)
async def test_small_length_fingerprint(
    auth_postgres_service: AuthService,
    insert_first_user: models.User,
    first_user: models.User,
    fingerprint: str,
):

    with pytest.raises(ValidationError):
        await auth_postgres_service.check_user_password(
            cmd=models.AuthCommand(
                username=first_user.username,
                password=first_user.password.get_secret_value(),
                fingerprint=fingerprint,
            ),
        )
