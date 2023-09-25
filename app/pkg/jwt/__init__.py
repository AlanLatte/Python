from dependency_injector import containers, providers
from dependency_injector.providers import Singleton

from app.pkg.models.exceptions.jwt import TokenTimeExpired, UnAuthorized, WrongToken
from app.pkg.settings import settings
from .access import JwtAccessBearer
from .credentionals import JwtAuthorizationCredentials
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


access_security = JwtAccessBearer(secret_key=settings.API.JWT.SECRET_KEY)

refresh_security = JwtRefreshBearer(
    secret_key=settings.API.JWT.SECRET_KEY,
)


class JWT(containers.DeclarativeContainer):
    """Dependency factory injector for JWT."""

    access: Singleton[JwtAccessBearer] = providers.Singleton(
        JwtAccessBearer,
        secret_key=settings.API.JWT.SECRET_KEY,
    )
    refresh: Singleton[JwtRefreshBearer] = providers.Singleton(
        JwtRefreshBearer,
        secret_key=settings.API.JWT.SECRET_KEY,
    )
