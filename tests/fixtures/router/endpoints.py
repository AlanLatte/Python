import pytest


@pytest.fixture()
async def user_router() -> str:
    return "/user"


@pytest.fixture()
async def auth_router() -> str:
    return "/auth"
