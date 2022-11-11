from fastapi import status

from app.pkg.models.base import BaseException

__all__ = [
    "UnAuthorized",
    "TokenTimeExpired",
    "WrongToken",
    "CSRFError",
    "JWTDecodeError",
]


class UnAuthorized(BaseException):
    message = "Not authorized"
    status_code = status.HTTP_401_UNAUTHORIZED


class TokenTimeExpired(BaseException):
    def __init__(self, message: Exception = None):
        if message:
            self.message = f"Token time expired: {message}"

    message = "Token time expired"
    status_code = status.HTTP_401_UNAUTHORIZED


class WrongToken(BaseException):
    def __init__(self, message: Exception = None):
        if message:
            self.message = f"Wrong token: {message}"

    message = "Wrong token"
    status_code = status.HTTP_401_UNAUTHORIZED


class CSRFError(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = "CSRF double submit tokens do not match"


class JWTDecodeError(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = "Missing claim: csrf"
