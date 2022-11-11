"""All connectors in declarative container."""

from dependency_injector import containers, providers

from app.pkg.settings import settings

from .mysql import Mysql
from .postgresql import Postgresql
from .sqlite import SQLite

__all__ = ["Connectors", "SQLite", "Postgresql", "Mysql"]


class Connectors(containers.DeclarativeContainer):
    """Declarative container with connectors."""

    configuration = providers.Configuration(
        name="settings",
        pydantic_settings=[settings],
    )

    postgresql = providers.Factory(
        Postgresql,
        username=configuration.POSTGRES_USER,
        password=configuration.POSTGRES_PASSWORD,
        host=configuration.POSTGRES_HOST,
        port=configuration.POSTGRES_PORT,
        database_name=configuration.POSTGRES_DATABASE_NAME,
    )

    # sqlite = providers.Factory(SQLite, sqlite_path=configuration.SQLITE_PATH)
    # mysql = providers.Factory(
    #     Mysql,
    #     username=configuration.POSTGRES_USER,
    #     password=configuration.POSTGRES_PASSWORD,
    #     host=configuration.POSTGRES_HOST,
    #     port=configuration.POSTGRES_PORT,
    #     database_name=configuration.POSTGRES_DATABASE_NAME,
    # )
