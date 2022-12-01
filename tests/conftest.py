from app.configuration import __containers__
from app.pkg.connectors import Connectors

pytest_plugins = [
    "tests.fixtures.repository.postgresql.postgresql_fixtures",
    "tests.fixtures.repository.postgresql.repositories",
    "tests.fixtures.repository.postgresql.user",
    "tests.fixtures.settings_fixtures",
    "tests.fixtures.models.user",
    # path to module with fixtures.
]


def pytest_sessionstart(session):
    _ = session

    __containers__.set_environment(
        connector_class=Connectors, pkg_name=__name__, testing=True
    )
