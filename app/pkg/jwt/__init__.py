from dependency_injector import containers, providers

from app.pkg.settings import settings

from .access import JwtAccessBearer
from .credentionals import JwtAuthorizationCredentials
from .exceptions import TokenTimeExpired, UnAuthorized, WrongToken
from .refresh import JwtRefreshBearer

__all__ = [
    "JWT",
    "JwtAuthorizationCredentials",
    "JwtAccessBearer",
    "JwtRefreshBearer",
    "access_security",
    "refresh_security",
    "UnAuthorized",
    "TokenTimeExpired",
    "WrongToken",
]


access_security = JwtAccessBearer(secret_key=settings.JWT_SECRET_KEY.get_secret_value())

refresh_security = JwtRefreshBearer(
    secret_key=settings.JWT_SECRET_KEY.get_secret_value(),
)


class JWT(containers.DeclarativeContainer):
    """Dependency factory injector for JWT."""

    access: JwtAccessBearer = providers.Factory(
        JwtAccessBearer,
        secret_key=settings.JWT_SECRET_KEY.get_secret_value(),
    )
    refresh: JwtRefreshBearer = providers.Factory(
        JwtRefreshBearer,
        secret_key=settings.JWT_SECRET_KEY.get_secret_value(),
    )
