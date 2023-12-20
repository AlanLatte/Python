"""Configuration for pytest."""

import asyncio

import pytest

from app.configuration import __containers__
from app.pkg.connectors import PostgresSQL

pytest_plugins = [
    "tests.fixtures.repository.postgresql.repositories",
    "tests.fixtures.repository.postgresql.postgresql",
    "tests.fixtures.repository.postgresql.inserters",
    "tests.fixtures.services.services",
    "tests.fixtures.router.client",
    "tests.fixtures.router.endpoints",
    "tests.fixtures.router.responses",
    "tests.fixtures.models.controller",
    "tests.fixtures.models.generators",
    "tests.fixtures.handlers.equals",
    "tests.fixtures.settings",
    # path to module with fixtures.
]

pytestmark = pytest.mark.anyio


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case.

    Notes:
        This fixture is used for anyio tests.

    Warnings:
        Full isolation for each test case is guaranteed only if the test cases
        are executed sequentially.
    """

    _ = request
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


def pytest_sessionstart(session):
    _ = session

    __containers__.set_environment(
        connectors=[PostgresSQL],
        pkg_name="tests",
        testing=True,
    )
