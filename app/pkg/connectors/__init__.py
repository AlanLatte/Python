"""All connectors in declarative container."""

from dependency_injector import containers, providers
from app.pkg.settings import settings

__all__ = ["Connectors"]


class Connectors(containers.DeclarativeContainer):
    """Declarative container with connectors."""

    configuration = providers.Configuration(
        name="settings", pydantic_settings=[settings]
    )
