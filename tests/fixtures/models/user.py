from dataclasses import dataclass

import pytest

from app.pkg import models


@dataclass
class User:
    inserted: models.User
    raw: models.User


@pytest.fixture()
async def first_user() -> models.User:
    return models.User(
        id=1,
        username="correct-user-1@example.ru",
        password=b"supeR_%$tr0ng-pa$$worD",
        role_name=models.UserRole.USER,
    )


@pytest.fixture()
async def second_user() -> models.User:
    return models.User(
        id=1,
        username="correct-user-2@example.ru",
        password=b"supeR_%$tr0ng-pa$$worD",
        role_name=models.UserRole.USER,
    )
