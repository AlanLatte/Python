from dependency_injector import containers, providers

from app.pkg.settings import settings

from .resource import Postgresql

__all__ = ["PostgresSQL"]


class PostgresSQL(containers.DeclarativeContainer):
    """Declarative container with connectors."""

    configuration = providers.Configuration(
        name="settings",
        pydantic_settings=[settings],
    )

    connector = providers.Resource(Postgresql, dsn=configuration.POSTGRES.DSN)
