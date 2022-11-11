from typing import Any, Dict, Optional

__all__ = ["JwtAuthorizationCredentials"]


class JwtAuthorizationCredentials:
    def __init__(
        self,
        subject: Dict[str, Any],
        raw_token: str,
        jti: Optional[str] = None,
    ):
        self.subject = subject
        self.jti = jti
        self.raw_token = raw_token

    def __getitem__(self, item: str) -> Any:
        return self.subject[item]
