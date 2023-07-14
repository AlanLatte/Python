"""All connectors in declarative container."""

from dependency_injector import containers, providers

from app.pkg.settings import settings

from .postgresql import Postgresql

__all__ = ["Connectors", "Postgresql"]


class Connectors(containers.DeclarativeContainer):
    """Declarative container with connectors."""

    configuration = providers.Configuration(
        name="settings",
        pydantic_settings=[settings],
    )

    postgresql = providers.Factory(
        Postgresql,
        username=configuration.POSTGRES.USER,
        password=configuration.POSTGRES.PASSWORD,
        host=configuration.POSTGRES.HOST,
        port=configuration.POSTGRES.PORT,
        database_name=configuration.POSTGRES.DATABASE_NAME,
    )
