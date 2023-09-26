"""User models fixtures."""

from dataclasses import dataclass
from typing import Any, Callable, Coroutine

import pytest
from jsf import JSF

from app.pkg import models


@dataclass
class User:
    inserted: models.User
    raw: models.User


@pytest.fixture()
def new_user_generator() -> Callable[[], Any]:
    mock_user = JSF(models.User.schema())

    def generate() -> Any:
        return models.User(**mock_user.generate())

    return generate


@pytest.fixture()
async def first_user(
    new_user_generator,  # pylint: disable=redefined-outer-name
) -> Coroutine[Any, Any, User]:
    return new_user_generator()


@pytest.fixture()
async def second_user(
    new_user_generator,  # pylint: disable=redefined-outer-name
) -> Coroutine[Any, Any, User]:
    return new_user_generator()
