import pytest
from starlette import status

from app.pkg.models.exceptions.repository import EmptyResult
from tests.fixtures.router.client import Client


@pytest.mark.skip(reason="Not implemented")
@pytest.mark.correct
async def test_user_in_database(
    authorized_first_client: Client,
    user_router: str,
    response_equal,
):
    response = await authorized_first_client.request(
        method="DELETE",
        url=f"{user_router}/{authorized_first_client.user.inserted.id}",
    )

    assert response_equal(
        response=response,
        model=authorized_first_client.user.inserted,
        expected_status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        exclude_from_model=["password"],
    )


@pytest.mark.skip(reason="Not implemented")
@pytest.mark.incorrect
async def test_user_not_found(
    authorized_first_client: Client,
    user_router: str,
    response_with_error,

):
    response = await authorized_first_client.request(
        method="DELETE",
        url=f"{user_router}/{authorized_first_client.user.inserted.id+1}",
    )
    response_with_error(response=response, model=EmptyResult)


@pytest.mark.skip(reason="Not implemented")
@pytest.mark.incorrect
async def test_access_token_not_exists():
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented")
@pytest.mark.incorrect
async def test_signature_token_error():
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented")
@pytest.mark.incorrect
async def test_sending_refresh_token():
    raise NotImplementedError
