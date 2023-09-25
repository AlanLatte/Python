from dependency_injector import containers, providers

from app.pkg.settings import settings

from app.pkg.connectors.postgresql.resource import Postgresql

__all__ = ["PostgresSQL"]


class PostgresSQL(containers.DeclarativeContainer):
    """Declarative container with PostgresSQL connector."""

    configuration = providers.Configuration(
        name="settings",
        pydantic_settings=[settings],
    )

    connector = providers.Resource(
        Postgresql,
        dsn=configuration.POSTGRES.DSN,
        minsize=configuration.POSTGRES.MIN_CONNECTION,
        maxsize=configuration.POSTGRES.MAX_CONNECTION,
    )
