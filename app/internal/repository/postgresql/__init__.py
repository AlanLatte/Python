from dependency_injector import containers, providers
from .user import User


class Repository(containers.DeclarativeContainer):
    user = providers.Factory(User)
