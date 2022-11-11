from typing import Literal

import httpx
import pydantic

__all__ = ["HttpRequests"]

from app.pkg.models.exceptions.client import ClientException
from app.pkg.logger import get_logger


class HttpRequests:
    client_name: str
    AUTH_X_TOKEN: pydantic.SecretStr
    url: pydantic.AnyUrl

    def __init__(self, x_token: pydantic.SecretStr, url: pydantic.AnyUrl, client_name: str):
        self.AUTH_X_TOKEN = x_token
        self.url = url
        self.client_name = client_name
        self.logger = get_logger(self.client_name)

    async def do_request(
            self, method: Literal["GET", "POST"], path: str = None, **kwargs
    ) -> httpx.Response:
        async with httpx.AsyncClient(
                headers={"X-ACCESS-TOKEN": self.AUTH_X_TOKEN.get_secret_value()},
        ) as client:
            try:
                response = await client.request(
                    method=method, url=f"{self.url}/{path}", **kwargs
                )
            except Exception as e:
                self.logger.exception("exception: %s" % e)
                raise ClientException(message="%s is not available now" % self.client_name)

            if response.is_success:
                return response
            else:
                self.logger.exception("status: %s" % response)
                raise ClientException(message="%s is not available now" % self.client_name)
