from app.pkg.models.base import BaseAPIException

__all__ = [
    "IncorrectLengthFingerprint",
    "IncorrectUsernameOrPassword",
]


class IncorrectLengthFingerprint(BaseAPIException):
    status_code = 400
    message = "Incorrect fingerprint"


class IncorrectUsernameOrPassword(BaseAPIException):
    status_code = 406
    message = "Incorrect username or password or secret key"
