from starlette import status

from app.pkg import models
from app.pkg.models.exceptions.jwt import UnAuthorized, WrongToken
from app.pkg.settings.settings import Settings
from tests.fixtures.router.client import Client


async def test_correct(
    authorized_first_client: Client,
    auth_router: str,
    fist_auth_user: models.AuthCommand,
):
    authorized_first_client.set_auth_header(use_access=False)

    response = await authorized_first_client.request(
        method="POST", url=f"{auth_router}/logout", json=fist_auth_user
    )
    assert response.status_code == status.HTTP_200_OK


async def test_incorrect_refresh_token(
    authorized_first_client: Client,
    auth_router: str,
    response_without_error,
    fist_auth_user: models.User,
    settings: Settings,
):
    authorized_first_client.set_auth_header(use_access=False)
    response = await authorized_first_client.request(
        method="POST",
        url=f"{auth_router}/logout",
        json=fist_auth_user,
    )

    assert response.status_code == status.HTTP_200_OK

    response = await authorized_first_client.request(
        method="POST",
        url=f"{auth_router}/logout",
        json=fist_auth_user,
    )

    assert response_without_error(response, UnAuthorized, relative_occurrence=True)
