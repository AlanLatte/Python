import pytest
from starlette import status

from app.pkg import models
from app.pkg.models.exceptions.jwt import UnAuthorized
from app.pkg.models.exceptions.user import UserAlreadyExist
from tests.fixtures.router.client import Client


@pytest.mark.correct
async def test_create_user_with_admin_role(
    authorized_first_client: Client,
    second_user: models.User,
    user_router: str,
    response_equal,
):
    response = await authorized_first_client.request(
        method="POST",
        url=f"{user_router}/",
        json=second_user.migrate(models.CreateUserCommand),
    )

    assert response_equal(
        response=response,
        model=second_user,
        expected_status_code=status.HTTP_201_CREATED,
        exclude_from_model=["id", "password"],
    )


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
@pytest.mark.incorrect
async def test_password_length(
    authorized_first_client: Client,
    second_user: models.User,
    user_router: str,
    password: str,
    response_with_error,
):

    response = await authorized_first_client.request(
        method="POST",
        url=f"{user_router}/",
        json=second_user.migrate(models.CreateUserCommand),
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.incorrect
async def test_unique_violation(
    authorized_first_client: Client,
    second_user: models.User,
    user_router: str,
    response_with_error,
    response_equal,
):
    response = await authorized_first_client.request(
        method="POST",
        url=f"{user_router}/",
        json=second_user.migrate(models.CreateUserCommand),
    )

    assert response_equal(
        response=response,
        model=second_user,
        expected_status_code=status.HTTP_201_CREATED,
        exclude_from_model=["id", "password"],
    )

    response = await authorized_first_client.request(
        method="POST",
        url=f"{user_router}/",
        json=second_user.migrate(models.CreateUserCommand),
    )

    assert response_with_error(response=response, model=UserAlreadyExist)


@pytest.mark.incorrect
async def test_unauthorized_request(
    client: Client, second_user: models.User, user_router: str, response_with_error
):
    response = await client.request(
        method="POST",
        url=f"{user_router}/",
        json=second_user.migrate(models.CreateUserCommand),
    )

    assert response_with_error(response=response, model=UnAuthorized)
