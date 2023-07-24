from dependency_injector import containers, providers

from app.pkg.settings import settings
from .postgresql import Postgresql

__all__ = ["PostgresSQL"]


class PostgresSQL(containers.DeclarativeContainer):
    """Declarative container with connectors."""

    configuration = providers.Configuration(
        name="settings",
        pydantic_settings=[settings],
    )

    postgresql = providers.Factory(
        Postgresql,
        postgres_dsn=configuration.POSTGRES.DSN
    )

