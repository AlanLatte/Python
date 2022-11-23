import pytest
from dependency_injector.wiring import Provide, inject

from app.internal.repository.postgresql import Repository
from app.internal.repository.postgresql.user import User


@pytest.fixture()
async def user_repository(
    overwrite_connection,
) -> User:
    return await __get_user_repository()


@inject
async def __get_user_repository(user: User = Provide[Repository.user]):
    return user
