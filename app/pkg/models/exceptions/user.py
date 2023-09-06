from fastapi import status

from app.pkg.models.base import BaseAPIException

__all__ = ["UserAlreadyExist", "IncorrectOldPassword", "IncorrectPasswordLength"]


class UserAlreadyExist(BaseAPIException):
    message = "User already exist."
    status_code = status.HTTP_409_CONFLICT


# TODO: Raise this in validator.
class IncorrectPasswordLength(BaseAPIException):
    message = "Incorrect password length"
    status_code = status.HTTP_400_BAD_REQUEST


class IncorrectOldPassword(BaseAPIException):
    message = "Incorrect old password."
    status_code = status.HTTP_400_BAD_REQUEST


class UserNotFound(BaseAPIException):
    message = "User not found."
    status_code = status.HTTP_404_NOT_FOUND


class UserAlreadyActivated(BaseAPIException):
    message = "User already activated."
    status_code = status.HTTP_409_CONFLICT
