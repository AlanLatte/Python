"""All postgresql repositories are defined here."""

from dependency_injector import containers, providers

from app.internal.repository.postgresql.refresh_tokens import JWTRefreshTokenRepository
from app.internal.repository.postgresql.user import UserRepository
from app.internal.repository.postgresql.user_roles import UserRoleRepository


class Repositories(containers.DeclarativeContainer):
    """Container for postgresql repositories."""

    user_repository = providers.Factory(UserRepository)
    refresh_token_repository = providers.Factory(JWTRefreshTokenRepository)
    user_role_repository = providers.Factory(UserRoleRepository)
