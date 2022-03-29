import pytest
from app.internal.repository.postgresql import Repository
from app.internal.repository.postgresql.user import User
from dependency_injector.wiring import inject, Provide


@pytest.fixture()
async def user_repository(
    overwrite_connection,
) -> User:
    return await __get_user_repository()


@inject
async def __get_user_repository(user: User = Provide[Repository.user]):
    return user
