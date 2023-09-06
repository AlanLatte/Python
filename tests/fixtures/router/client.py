import typing

import httpx
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, Response

from app import create_app
from app.pkg import models
from app.pkg.models.base import BaseModel, Model
from app.pkg.settings import Settings
from tests.fixtures.models.user import User


class Client:
    client: typing.Union[AsyncClient, TestClient]
    refresh_token: typing.Optional[str] = None
    access_token: typing.Optional[str] = None
    user: typing.Optional[User]

    def __init__(
        self,
        client: typing.Union[AsyncClient, TestClient],
        refresh_token: typing.Optional[str] = None,
        access_token: typing.Optional[str] = None,
        user: typing.Optional[User] = None,
    ):
        self.client = client
        self.refresh_token = refresh_token
        self.access_token = access_token
        self.user = user

    @staticmethod
    def __build_auth_headers(token: typing.Optional[str] = None) -> httpx.Headers:
        if not token:
            raise AttributeError("Token not given")

        return httpx.Headers(headers={"Authorization": f"Bearer {token}"})

    def set_auth_header(
        self,
        use_access: bool = True,
        token: typing.Optional[str] = None,
    ):
        if use_access and token:
            self.access_token = token
        elif not use_access and token:
            self.refresh_token = token

        if use_access and not token:
            token = self.access_token
        elif not use_access and not token:
            token = self.refresh_token

        self.client.headers = self.__build_auth_headers(token=token)

    async def request(
        self,
        method: str,
        url: str,
        *,
        json: typing.Union[
            Model,
            typing.Dict[str, typing.Union[str, int, float]],
            None,
        ] = None,
        headers: typing.Optional[typing.Dict[str, str]] = None,
        **kwargs,
    ) -> Response:
        if isinstance(json, BaseModel):
            json = json.to_dict(show_secrets=True)

        return await self.client.request(
            method=method,
            url=url,
            json=json,
            headers=headers,
            **kwargs,
        )


@pytest.fixture()
async def client() -> typing.AsyncIterator[Client]:
    async with AsyncClient(app=create_app(), base_url="http://test") as client:
        yield Client(client=client)


@pytest.fixture()
async def authorized_first_client(
    client: Client,
    insert_first_user: models.User,
    auth_router: str,
    first_user: models.User,
    settings: Settings,
    create_model,
) -> Client:
    response = await client.request(
        method="POST",
        url=f"{auth_router}/login",
        json=first_user.migrate(models.AuthCommand, random_fill=True),
    )

    assert response.status_code == 200

    json_response: typing.Dict[str, str] = response.json()

    client.user = User(inserted=insert_first_user, raw=first_user)
    client.refresh_token = json_response.get(settings.API.JWT.REFRESH_TOKEN_NAME)
    client.access_token = json_response.get(settings.API.JWT.ACCESS_TOKEN_NAME)

    client.set_auth_header()

    return client
