"""Fixture for buildint error response given from API."""


import typing

import httpx
import pytest

from app.pkg.models.base import BaseAPIException, Model
from tests.types.responses import ErrorCheckerType, ResponseEqual


@pytest.fixture(name="build_error_response")
async def build_error_response_fixture():
    return lambda model: {"message": model.message}


@pytest.fixture()
def response_with_error(build_error_response) -> ErrorCheckerType:
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

                >>> ...  # Imports and etc...
                >>> async def test_correct_user_creation(client: Client):
                ...    response = await client.request(
                ...         method="POST",
                ...         url="/users",
                ...         json={
                ...             "username": "kitty",
                ...             "password": "SuperStrongPa$$w0rd",
                ...             "role_name": "simple_cat"
                ...         }
                >>>     )
                >>> assert response_with_error(response, IncorrectRoleName)

            Sometimes it happens that the error is generated dynamically. Like a
            `WrongRoleName` exception. In such cases, a strict comparison of the request
            body may result in an `AssertionError`. To avoid this, you need to use
            the `relative_occurrence` True flag
                >>> from starlette import status
                >>> class WrongRoleName(BaseAPIException):
                ...    def __init__(self, message: Exception = None):
                ...        if message:
                ...            self.message = f"Wrong role name: {message}"
                >>>
                ...    message = "Wrong role"
                ...    status_code = status.HTTP_400_BAD_REQUEST
                >>>
                >>> async def test_correct_user_creation(client: Client):
                >>>    response = await client.request(
                >>>            method="POST",
                >>>            url="/users",
                >>>            json={
                >>>             "username": "kitty",
                >>>             "password": "SuperStrongPa$$w0rd",
                >>>             "role_name": "simple_cat"
                >>>         }
                >>>    )
                >>>
                >>> assert response_with_error(response, WrongRoleName, True)

        Returns:
            Boolean that False if asserts in them results in errors.
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


@pytest.fixture()
def response_equal() -> ResponseEqual:
    def wrapped(
        response: httpx.Response,
        model: Model,
        expected_status_code: int,
        exclude_from_model: typing.Optional[typing.List[str]] = None,
    ) -> bool:
        """Checking for equivalence between the model and the request that
        comes from the API.

        Args:
            response: httpx Client response.
            model: Target error model. Must be inherited from `BaseModel`
            expected_status_code: Response expected status code.
            exclude_from_model: If the model contains elements that do not need to be
                compared when checking for equivalence, you must specify in this
                argument, separated by commas in the string representation,
                the attributes of the model

        Examples:
            When you need to check response and model, use::

            async def test_correct(client: Client):
                response = await client.get("/users")
                assert response_equal(response, models.User, 200)

            When you need to check equal without specific model attribute, use::

            async def test_correct(client: Client):
                response = await client.get("/users")
                assert response_equal(response, models.User, 200, ["password"])

        Returns:
            Boolean that False if asserts in them results in errors.
        """

        try:
            assert response.status_code == expected_status_code

            json_response = response.json()
            json_model = model.to_dict(show_secrets=True)

            if exclude_from_model:
                __delete_keys_from_json(
                    json_model=json_model,
                    json_response=json_response,
                    exclude_from_model=exclude_from_model,
                )

            assert json_response == json_model
        except AssertionError:
            return False
        else:
            return True

    return wrapped


def __delete_keys_from_json(
    json_model: typing.Dict,
    json_response: typing.Dict,
    exclude_from_model: typing.List[str],
):
    """Mutate arguments and del from them items from `exclude_from_model`"""

    for exclude_item in exclude_from_model:
        try:
            del json_model[exclude_item]
            del json_response[exclude_item]
        except KeyError:
            pass
