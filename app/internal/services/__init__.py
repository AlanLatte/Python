from dependency_injector import containers, providers

from app.internal.repository import Repositories
from app.internal.services import auth, user
from app.internal.services.auth import AuthService
from app.internal.services.user import UserService
from app.pkg.otp.otp import OTPService
from app.pkg.settings import settings


class Services(containers.DeclarativeContainer):
    """Containers with services."""
    configuration = providers.Configuration(
        name="settings",
        pydantic_settings=[settings],
    )

    repositories = providers.Container(Repositories.postgres)

    #: OTP service
    otp_service = providers.Factory(OTPService, otp_key=configuration.OTP_KEY)

    user_service = providers.Factory(UserService, repositories.user_repository)

    auth_service = providers.Factory(
        AuthService,
        otp_service=otp_service,
        user_service=user_service,
        refresh_token_repository=repositories.refresh_token_repository,
    )
