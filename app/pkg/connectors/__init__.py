"""All connectors in declarative container."""

from dependency_injector import containers, providers

from .postgresql import PostgresSQL
from .resourсes import AsyncResource

__all__ = ["Connectors", "PostgresSQL"]


class Connectors(containers.DeclarativeContainer):
    """Declarative container with connectors."""

    postgres: PostgresSQL = providers.Container(PostgresSQL)

    postgresql = providers.Resource(
        AsyncResource,
        connector=postgres.postgresql,
        maxsize=250,
    )
