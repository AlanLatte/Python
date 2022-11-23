from typing import Any, Dict, Optional

from app.pkg.models.types import NotEmptySecretStr

__all__ = ["JwtAuthorizationCredentials"]


class JwtAuthorizationCredentials:
    subject: Dict[str, Any]
    raw_token: NotEmptySecretStr
    jti: Optional[str]

    def __init__(
        self,
        subject: Dict[str, Any],
        raw_token: NotEmptySecretStr,
        jti: Optional[str] = None,
    ):
        self.subject = subject
        self.jti = jti
        self.raw_token = raw_token

    def __getitem__(self, item: str) -> Any:
        return self.subject[item]
