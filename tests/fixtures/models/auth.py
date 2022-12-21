import pytest

from app.pkg import models


@pytest.fixture()
async def fist_auth_user(
    insert_first_user: models.User, first_user: models.User, first_fingerprint: str
):
    return models.AuthCommand(
        username=first_user.username,
        password=first_user.password.get_secret_value(),
        fingerprint=first_fingerprint,
    )


@pytest.fixture()
async def second_auth_user(
    insert_second_user: models.User, second_user: models.User, second_fingerprint: str
):
    return models.AuthCommand(
        username=second_user.username,
        password=second_user.password.get_secret_value(),
        fingerprint=second_fingerprint,
    )
