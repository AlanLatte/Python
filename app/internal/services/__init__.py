from dependency_injector import containers, providers

from app.internal.repository import Repositories, postgresql
from app.internal.services import auth, user
from app.internal.services.auth import AuthService
from app.internal.services.user import UserService
from app.internal.services.user_roles import UserRoleService


class Services(containers.DeclarativeContainer):
    """Containers with services."""

    repositories: postgresql.Repositories = providers.Container(
        Repositories.postgres,
    )  # type: ignore

    user_service = providers.Factory(UserService, repositories.user_repository)

    auth_service = providers.Factory(
        AuthService,
        user_service=user_service,
        refresh_token_repository=repositories.refresh_token_repository,
    )

    user_role_service = providers.Factory(
        UserRoleService,
        user_role_repository=repositories.user_role_repository,
    )
