from dataclasses import dataclass
from typing import Any, Callable, Coroutine

import pytest

from app.pkg import models


@dataclass
class User:
    inserted: models.User
    raw: models.User


@pytest.fixture()
def new_user_generator(create_model) -> Callable[..., Coroutine[Any, Any, Any]]:

    def generate() -> Any:
        return create_model(models.User)

    return generate


@pytest.fixture()
async def first_user(new_user_generator) -> Coroutine[Any, Any, User]:
    return await new_user_generator()


@pytest.fixture()
async def second_user(new_user_generator) -> Coroutine[Any, Any, User]:
    return await new_user_generator()
