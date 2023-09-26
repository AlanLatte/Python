"""Auth model fixtures."""

import pytest

from app.pkg import models


@pytest.fixture()
async def fist_auth_user(insert_first_user: models.User, first_user: models.User):
    del insert_first_user  # pylint: disable=unused-variable

    return first_user.migrate(models.AuthCommand, random_fill=True)


@pytest.fixture()
async def second_auth_user(insert_second_user: models.User, second_user: models.User):
    del insert_second_user  # pylint: disable=unused-variable

    return second_user.migrate(models.AuthCommand, random_fill=True)
