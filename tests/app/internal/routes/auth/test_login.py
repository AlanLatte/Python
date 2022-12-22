import uuid

import pytest
from starlette import status

from app.pkg import models
from app.pkg.models import UserRole
from app.pkg.models.exceptions.auth import IncorrectUsernameOrPassword
from app.pkg.models.exceptions.repository import EmptyResult
from app.pkg.settings.settings import Settings
from tests.fixtures.router.client import Client


async def test_correct_sign_by_one_fingerprint(
    client: Client,
    auth_router: str,
    fist_auth_user: models.AuthCommand,
    settings: Settings,
):
    response = await client.request(
        method="POST",
        url=f"{auth_router}/login",
        json=fist_auth_user,
    )
    assert response.status_code == status.HTTP_200_OK

    response_json = response.json()
    assert response_json.get(settings.JWT_ACCESS_TOKEN_NAME)
    assert response_json.get(settings.JWT_REFRESH_TOKEN_NAME)
    assert response_json.get("role_name") == UserRole.USER.value


@pytest.mark.parametrize(
    "password",
    [
        "1",
        "12",
        "123",
        "1234",
        "12345",
    ],
)
async def test_incorrect_sign_by_small_password_length(
    client: Client,
    auth_router: str,
    fist_auth_user: models.AuthCommand,
    settings: Settings,
    password: str,
):
    response = await client.request(
        method="POST",
        url=f"{auth_router}/login",
        json={
            "username": fist_auth_user.username,
            "password": password,
            "fingerprint": fist_auth_user.fingerprint.get_secret_value(),
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "cmd",
    [
        models.AuthCommand(
            username=uuid.uuid4().__str__(),
            password=uuid.uuid4().__str__(),
            fingerprint=uuid.uuid4().__str__(),
        ),
        models.AuthCommand(
            username=uuid.uuid4().__str__(),
            password=uuid.uuid4().__str__(),
            fingerprint=uuid.uuid4().__str__(),
        ),
        models.AuthCommand(
            username=uuid.uuid4().__str__(),
            password=uuid.uuid4().__str__(),
            fingerprint=uuid.uuid4().__str__(),
        ),
        models.AuthCommand(
            username=uuid.uuid4().__str__(),
            password=uuid.uuid4().__str__(),
            fingerprint=uuid.uuid4().__str__(),
        ),
        models.AuthCommand(
            username=uuid.uuid4().__str__(),
            password=uuid.uuid4().__str__(),
            fingerprint=uuid.uuid4().__str__(),
        ),
    ],
)
async def test_incorrect_user_not_found(
    client: Client, cmd: models.AuthCommand, auth_router: str, response_with_error
):
    response = await client.request(
        method="POST",
        url=f"{auth_router}/login",
        json=models.AuthCommand(
            username=uuid.uuid4().__str__(),
            password=uuid.uuid4().__str__(),
            fingerprint=uuid.uuid4().__str__(),
        ),
    )

    assert response_with_error(response, EmptyResult)


@pytest.mark.parametrize(
    "password",
    [
        uuid.uuid4().__str__(),
        uuid.uuid4().__str__(),
        uuid.uuid4().__str__(),
        uuid.uuid4().__str__(),
    ],
)
async def test_incorrect_user_incorrect_username(
    client: Client,
    auth_router: str,
    fist_auth_user: models.AuthCommand,
    response_with_error,
    password: str,
):
    response = await client.request(
        method="POST",
        url=f"{auth_router}/login",
        json=models.AuthCommand(
            username=fist_auth_user.username,
            password=password,
            fingerprint=fist_auth_user.fingerprint,
        ),
    )

    assert response_with_error(response, IncorrectUsernameOrPassword)


@pytest.mark.parametrize(
    "switch_fingerprint",
    [
        uuid.uuid4().__str__(),
        uuid.uuid4().__str__(),
        uuid.uuid4().__str__(),
        uuid.uuid4().__str__(),
        uuid.uuid4().__str__(),
    ],
)
async def test_correct_sign_by_two_fingerprints(
    client: Client,
    auth_router: str,
    fist_auth_user: models.AuthCommand,
    switch_fingerprint: str,
):
    response = await client.request(
        method="POST",
        url=f"{auth_router}/login",
        json=fist_auth_user,
    )
    assert response.status_code == status.HTTP_200_OK

    fist_auth_user = fist_auth_user.copy()

    fist_auth_user.fingerprint = switch_fingerprint
    response = await client.request(
        method="POST",
        url=f"{auth_router}/login",
        json=fist_auth_user,
    )

    assert response.status_code == status.HTTP_200_OK


async def test_incorrect_sign_by_two_devices_but_fingerprint_one(
    client: Client,
    auth_router: str,
    fist_auth_user: models.AuthCommand,
    first_fingerprint: str,
    settings: Settings,
):
    response_one = await client.request(
        method="POST",
        url=f"{auth_router}/login",
        json=fist_auth_user,
    )
    assert response_one.status_code == status.HTTP_200_OK

    fist_auth_user = fist_auth_user.copy()

    response_two = await client.request(
        method="POST",
        url=f"{auth_router}/login",
        json=fist_auth_user,
    )

    assert response_two.status_code == status.HTTP_200_OK

    one_json = response_two.json()
    two_device = response_one.json()

    assert (
        one_json[settings.JWT_REFRESH_TOKEN_NAME]
        == two_device[settings.JWT_REFRESH_TOKEN_NAME]
    )
    assert (
        one_json[settings.JWT_ACCESS_TOKEN_NAME]
        != two_device[settings.JWT_ACCESS_TOKEN_NAME]
    )
