"""All connectors in declarative container."""

from dependency_injector import containers, providers

from app.pkg.connectors.postgresql import PostgresSQL

__all__ = ["Connectors", "PostgresSQL"]


class Connectors(containers.DeclarativeContainer):
    """Declarative container with all connectors."""

    postgresql: PostgresSQL = providers.Container(PostgresSQL)
