from fastapi import status

from app.pkg.models.base import BaseAPIException

__all__ = [
    "UnAuthorized",
    "TokenTimeExpired",
    "WrongToken",
    "CSRFError",
    "JWTDecodeError",
]


class UnAuthorized(BaseAPIException):
    message = "Not authorized"
    status_code = status.HTTP_401_UNAUTHORIZED


class TokenTimeExpired(BaseAPIException):
    def __init__(self, message: Exception = None):
        if message:
            self.message = f"Token time expired: {message}"

    message = "Token time expired"
    status_code = status.HTTP_401_UNAUTHORIZED


class WrongToken(BaseAPIException):
    def __init__(self, message: Exception = None):
        if message:
            self.message = f"Wrong token: {message}"

    message = "Wrong token"
    status_code = status.HTTP_401_UNAUTHORIZED


class CSRFError(BaseAPIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = "CSRF double submit tokens do not match"


class JWTDecodeError(BaseAPIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = "Missing claim: csrf"
