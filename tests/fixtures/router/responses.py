import typing

import httpx
import pytest

from app.pkg.models.base import BaseAPIException
from tests.types.responses import ErrorCheckerType


@pytest.fixture
async def build_error_response():
    return lambda model: {"message": model.message}


@pytest.fixture()
def response_without_error(
    build_error_response: typing.Callable[
        [typing.Type[BaseAPIException]], typing.Dict[typing.Union[int, str], typing.Any]
    ],
) -> ErrorCheckerType:
    def check(
        response: httpx.Response,
        model: typing.Type[BaseAPIException],
        relative_occurrence: typing.Optional[bool] = False,
    ) -> bool:
        """Check if the request body response is valid.

        Args:
            response: Client response.
            model: Target error model. Must be inherited from `BaseAPIException`
            relative_occurrence: If true, use not strict comparison.

        Examples:
            When you have created a test and you need to check the response of a
            request against an error::

                ...  # Imports and etc...
                async def test_correct_user_creation(client: Client):
                    response = await client.request(method="POST", url="/users", json={
                        "username": "kitty",
                        "password": "SuperStrongPa$$w0rd",
                        "role_name": "simple_cat"
                    }

                    assert response_without_error(response, IncorrectRoleName)

            Sometimes it happens that the error is generated dynamically. Like a
            `WrongRoleName` exception. In such cases, a strict comparison of the request
            body may result in an `AssertionError`. To avoid this, you need to use
            the `relative_occurrence` True flag

                class WrongRoleName(BaseAPIException):
                    def __init__(self, message: Exception = None):
                        if message:
                            self.message = f"Wrong role name: {message}"

                    message = "Wrong role"
                    status_code = status.HTTP_400_BAD_REQUEST

                async def test_correct_user_creation(client: Client):
                    response = await client.request(method="POST", url="/users", json={
                        "username": "kitty",
                        "password": "SuperStrongPa$$w0rd",
                        "role_name": "simple_cat"
                    }

                    assert response_without_error(response, WrongRoleName, True)

        Returns:
            Wrapped function that returns False if asserts in them results in errors.
        """

        try:
            assert response.status_code == model.status_code
            if not relative_occurrence:
                assert response.json() == build_error_response(model)
            assert build_error_response(model)["message"] in response.json()["message"]
        except AssertionError:
            return False
        else:
            return True

    return check
