"""Service for auth methods."""

from typing import Optional

from app.internal.pkg.password import password
from app.internal.repository.postgresql import JWTRefreshTokenRepository
from app.internal.services.user import UserService
from app.pkg.jwt import UnAuthorized
from app.pkg.models.auth import AuthCommand
from app.pkg.models.exceptions.auth import IncorrectUsernameOrPassword
from app.pkg.models.exceptions.repository import EmptyResult, UniqueViolation
from app.pkg.models.refresh_token import (
    CreateJWTRefreshTokenCommand,
    DeleteJWTRefreshTokenCommand,
    JWTRefreshToken,
    ReadJWTRefreshTokenQuery,
    ReadJWTRefreshTokenQueryByFingerprint,
    UpdateJWTRefreshTokenCommand,
)
from app.pkg.models.user import ReadUserByUserNameQuery, User

__all__ = ["AuthService"]


class AuthService:

    #: JWTRefreshTokenRepository: JWTRefreshTokenRepository repository implementation.
    refresh_token_repository: JWTRefreshTokenRepository
    #: UserService: User service implementation.
    user_service: UserService

    def __init__(
        self,
        user_service: UserService,
        refresh_token_repository: JWTRefreshTokenRepository,
    ):
        """Initialize class for auth methods.

        Args:
            user_service:
                User interface implementation.
            refresh_token_repository:
                Refresh token interface implementation.
        """
        self.user_service = user_service
        self.refresh_token_repository = refresh_token_repository

    async def check_user_password(self, cmd: AuthCommand) -> User:
        """Check user password.

        Args:
            cmd:
                :class:`.AuthCommand`.

        Raises:
            IncorrectUsernameOrPassword: when username or password is incorrect.

        Returns:
            :class:`.User` model.
        """
        user = await self.user_service.read_specific_user_by_username(
            query=ReadUserByUserNameQuery(username=cmd.username),
        )
        if user is None or not password.check_password(cmd.password, user.password):
            raise IncorrectUsernameOrPassword

        return user

    async def check_user_exist_refresh_token(
        self,
        query: ReadJWTRefreshTokenQueryByFingerprint,
    ) -> Optional[JWTRefreshToken]:
        """Check user exist refresh token.

        Args:
            query:
                :class:`.ReadJWTRefreshTokenQueryByFingerprint`.

        Returns:
            :class:`.JWTRefreshToken` model.
            If a user does not exist refresh token, return `None`.
        """
        try:
            return await self.refresh_token_repository.read_by_fingerprint(
                query=query,
            )
        except EmptyResult:
            return None

    async def check_refresh_token_exists(
        self,
        query: ReadJWTRefreshTokenQuery,
    ) -> JWTRefreshToken:
        """Check refresh token exists.

        Args:
            query:
                :class:`.ReadJWTRefreshTokenQuery`.

        Raises:
            UnAuthorized:
                when refresh token does not exist.

        Returns:
            `JWTRefreshToken` model
        """
        try:
            return await self.refresh_token_repository.read(
                query=query,
            )
        except EmptyResult:
            raise UnAuthorized

    async def create_refresh_token(
        self,
        cmd: CreateJWTRefreshTokenCommand,
    ) -> JWTRefreshToken:
        """Create refresh token.

        Args:
            cmd:
                :class:`.CreateJWTRefreshTokenCommand`.

        Returns:
            `JWTRefreshToken` model.
            If a user exists, refresh token, then update data in database`.
        """
        try:
            return await self.refresh_token_repository.create(cmd=cmd)
        except UniqueViolation:
            return await self.refresh_token_repository.update(
                cmd=UpdateJWTRefreshTokenCommand(
                    user_id=cmd.user_id,
                    refresh_token=cmd.refresh_token,
                    fingerprint=cmd.fingerprint,
                ),
            )

    async def update_refresh_token(
        self,
        cmd: UpdateJWTRefreshTokenCommand,
    ) -> JWTRefreshToken:
        """Update refresh token.

        Args:
            cmd:
                :class:`.UpdateJWTRefreshTokenCommand`.

        Returns:
            :class:`.JWTRefreshToken` model.
        """
        return await self.refresh_token_repository.update(cmd)

    async def delete_refresh_token(
        self,
        cmd: DeleteJWTRefreshTokenCommand,
    ) -> JWTRefreshToken:
        """Delete refresh token.

        Args:
            cmd:
                :class:`.DeleteJWTRefreshTokenCommand`.

        Raises:
            UnAuthorized:
                when refresh token does not exist.

        Returns:
            :class:`.JWTRefreshToken` model.
        """
        try:
            return await self.refresh_token_repository.delete(
                cmd=cmd,
            )
        except EmptyResult:
            raise UnAuthorized
