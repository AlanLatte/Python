from fastapi import status

from app.pkg.models.base import BaseException


class UserAlreadyExist(BaseException):
    status_code = status.HTTP_409_CONFLICT
    message = "User already exist."


class IncorrectPasswordLength(BaseException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = "Incorrect password length"


class IncorrectOldPassword(BaseException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = "Incorrect old password."
