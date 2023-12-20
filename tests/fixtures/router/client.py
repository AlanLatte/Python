"""Module for contains."""

import typing

import httpx
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, Response

from app import create_app
from app.pkg.models.base import BaseModel, Model
from app.pkg.settings.settings import Settings


class Client:
    """Client for testing API."""

    client: typing.Union[AsyncClient, TestClient]

    def __init__(
        self,
        client: typing.Union[AsyncClient, TestClient],  # pylint: disable=W0621
    ):
        self.client = client

    @staticmethod
    def __build_auth_headers(token: typing.Optional[str] = None) -> httpx.Headers:
        if not token:
            raise AttributeError("Token not given")

        return httpx.Headers(headers={"X-ACCESS-TOKEN": token})

    def set_auth_header(
        self,
        token: typing.Optional[str] = None,
    ):
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
async def client() -> typing.AsyncIterator[Client]:  # pylint: disable=W0621
    async with AsyncClient(app=create_app(), base_url="http://test") as async_client:
        yield Client(client=async_client)


@pytest.fixture()
async def authorized_client(
    client: Client,
    settings: Settings,
) -> Client:
    client.set_auth_header(token=settings.API.X_ACCESS_TOKEN.get_secret_value())

    return client
