from dependency_injector import containers, providers

from app.internal.repository.postgresql import Repository
from .user import User

__all__ = ["Services", "User"]


class Services(containers.DeclarativeContainer):
    """Containers with services."""

    repository_container = providers.Container(Repository)

    user = providers.Factory(User, repository=repository_container.user)
