from datetime import timedelta
from typing import Optional, Set

from fastapi import Security
from jose import jwt
from pydantic import SecretStr

from app.pkg.jwt.base import JwtAuthBase
from app.pkg.jwt.credentionals import JwtAuthorizationCredentials
from app.pkg.models.types import NotEmptySecretStr

__all__ = ["JwtAccessBearer"]


class JwtAccess(JwtAuthBase):
    _bearer = JwtAuthBase.JwtAccessBearer()
    _cookie = JwtAuthBase.JwtAccessCookie()

    def __init__(
        self,
        secret_key: SecretStr,
        places: Optional[Set[str]] = None,
        auto_error: bool = True,
        algorithm: str = jwt.ALGORITHMS.HS256,
        access_expires_delta: Optional[timedelta] = None,
        refresh_expires_delta: Optional[timedelta] = None,
    ):
        super().__init__(
            secret_key.get_secret_value(),
            places=places,
            auto_error=auto_error,
            algorithm=algorithm,
            access_expires_delta=access_expires_delta,
            refresh_expires_delta=refresh_expires_delta,
        )

    async def _get_credentials(
        self,
        bearer: Optional[JwtAuthBase.JwtAccessBearer],
        cookie: Optional[JwtAuthBase.JwtAccessCookie],
    ) -> Optional[JwtAuthorizationCredentials]:
        payload, raw_token = await self._get_payload(bearer, cookie)

        if payload:
            return JwtAuthorizationCredentials(
                subject=payload["subject"],
                raw_token=NotEmptySecretStr(raw_token),
                jti=payload.get("jti", None),
            )
        return None


class JwtAccessBearer(JwtAccess):
    def __init__(
        self,
        secret_key: SecretStr,
        auto_error: bool = True,
        algorithm: str = jwt.ALGORITHMS.HS256,
        access_expires_delta: Optional[timedelta] = None,
        refresh_expires_delta: Optional[timedelta] = None,
    ):
        super().__init__(
            secret_key=secret_key,
            places={"header"},
            auto_error=auto_error,
            algorithm=algorithm,
            access_expires_delta=access_expires_delta,
            refresh_expires_delta=refresh_expires_delta,
        )

    async def __call__(
        self,
        bearer: JwtAuthBase.JwtAccessBearer = Security(JwtAccess._bearer),
    ) -> Optional[JwtAuthorizationCredentials]:
        return await self._get_credentials(bearer=bearer, cookie=None)
