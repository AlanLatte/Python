import pytest

from app.pkg import models


@pytest.fixture()
async def fist_auth_user(insert_first_user: models.User, first_user: models.User):
    return first_user.migrate(models.AuthCommand, random_fill=True)


@pytest.fixture()
async def second_auth_user(insert_second_user: models.User, second_user: models.User):
    return second_user.migrate(models.AuthCommand, random_fill=True)
