"""Fixtures for routes."""


import pytest

from app.internal.routes import city_router


@pytest.fixture()
async def city_route() -> str:
    return city_router.prefix
