import pytest

from app.configuration import __containers__
from app.pkg.connectors import Connectors

pytest_plugins = [
    "tests.fixtures.repository.postgresql.postgresql",
    "tests.fixtures.repository.postgresql.repositories",
    "tests.fixtures.repository.postgresql.user",
    "tests.fixtures.repository.postgresql.refresh_token",
    "tests.fixtures.services.postgresql.user",
    "tests.fixtures.services.postgresql.auth",
    "tests.fixtures.services.postgresql.user_role",
    "tests.fixtures.router.client",
    "tests.fixtures.router.endpoints",
    "tests.fixtures.router.responses",
    "tests.fixtures.models.user",
    "tests.fixtures.models.auth",
    "tests.fixtures.settings",
    # path to module with fixtures.
]

pytestmark = pytest.mark.anyio


def pytest_sessionstart(session):
    _ = session

    __containers__.set_environment(
        connector_class=Connectors,
        pkg_name=__name__,
        testing=True,
    )
