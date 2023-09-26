"""All connectors in declarative container."""

from dependency_injector import containers, providers

from .postgresql import PostgresSQL
from .resources import BaseAsyncResource

__all__ = ["Connectors", "PostgresSQL"]


class Connectors(containers.DeclarativeContainer):
    """Declarative container with all connectors."""

    postgresql: PostgresSQL = providers.Container(PostgresSQL)
