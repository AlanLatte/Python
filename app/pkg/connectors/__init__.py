"""All connectors in declarative container."""

from dependency_injector import containers, providers

from .postgresql import Postgresql
from app.pkg.settings import settings

__all__ = ["Connectors"]


class Connectors(containers.DeclarativeContainer):
    """Declarative container with connectors."""

    configuration = providers.Configuration(
        name="settings", pydantic_settings=[settings]
    )

    #: Postgresql: Connector to postgresql.
    postgresql = providers.Factory(
        Postgresql,
        username=configuration.POSTGRES_HOST,
        password=configuration.POSTGRES_PORT,
        host=configuration.POSTGRES_USER,
        port=configuration.POSTGRES_PASSWORD,
        database_name=configuration.POSTGRES_DATABASE_NAME,
    )
