from starlette import status

from app.pkg import models
from app.pkg.models.exceptions.jwt import UnAuthorized, WrongToken
from app.pkg.settings.settings import Settings
from tests.fixtures.router.client import Client


async def test_correct_new_token_pair(
    authorized_first_client: Client,
    first_user: models.User,
    auth_router: str,
    settings: Settings,
):
    authorized_first_client.set_auth_header(use_access=False)

    response = await authorized_first_client.request(
        method="PATCH", url=f"{auth_router}/refresh"
    )

    assert (
        authorized_first_client.refresh_token
        != response.json()[settings.JWT_REFRESH_TOKEN_NAME]
    )
    assert response.status_code == status.HTTP_200_OK


async def test_incorrect_old_token_not_usable(
    authorized_first_client: Client,
    first_user: models.User,
    auth_router: str,
    response_without_error,
    settings: Settings,
):
    authorized_first_client.set_auth_header(use_access=False)
    old_refresh_token = authorized_first_client.refresh_token

    response = await authorized_first_client.request(
        method="PATCH", url=f"{auth_router}/refresh"
    )

    assert response.status_code == status.HTTP_200_OK
    new_refresh_token = response.json()[settings.JWT_REFRESH_TOKEN_NAME]

    assert old_refresh_token != new_refresh_token

    response = await authorized_first_client.request(
        method="PATCH", url=f"{auth_router}/refresh"
    )

    assert response_without_error(response, UnAuthorized)

    authorized_first_client.set_auth_header(use_access=False, token=new_refresh_token)

    response = await authorized_first_client.request(
        method="PATCH", url=f"{auth_router}/refresh"
    )

    assert response.status_code == status.HTTP_200_OK


async def test_incorrect_token_signature(
    authorized_first_client: Client,
    first_user: models.User,
    auth_router: str,
    settings: Settings,
    response_without_error,
):
    authorized_first_client.set_auth_header(use_access=False, token="FAKE.SIGNATURE")
    response = await authorized_first_client.request(
        method="PATCH", url=f"{auth_router}/refresh"
    )

    assert response_without_error(response, WrongToken)