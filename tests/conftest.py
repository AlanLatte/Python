from app.configuration import __containers__
from app.pkg.connectors import Connectors

pytest_plugins = [
    "tests.fixtures.repository.postgresql.postgresql",
    "tests.fixtures.repository.postgresql.repositories",
    "tests.fixtures.repository.postgresql.user",
    "tests.fixtures.repository.postgresql.refresh_token",
    "tests.fixtures.services.postgresql.user",
    "tests.fixtures.services.postgresql.auth",
    "tests.fixtures.services.postgresql.user_roles",
    "tests.fixtures.router.app",
    "tests.fixtures.models.user",
    # path to module with fixtures.
]


def pytest_sessionstart(session):
    _ = session

    __containers__.set_environment(
        connector_class=Connectors,
        pkg_name=__name__,
        testing=True,
    )
