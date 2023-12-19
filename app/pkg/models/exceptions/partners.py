"""Exceptions for partners."""

from starlette import status

from app.pkg.models.base import BaseAPIException

__all__ = [
    "PartnerNameAlreadyExists",
    "PartnerTokenAlreadyExists",
    "PartnerNotFound",
]


class PartnerNameAlreadyExists(BaseAPIException):
    """Partner name already exists."""

    message = "Partner name already exists."
    status_code = status.HTTP_400_BAD_REQUEST


class PartnerTokenAlreadyExists(BaseAPIException):
    """Partner token already exists."""

    message = "Partner token already exists."
    status_code = status.HTTP_400_BAD_REQUEST


class PartnerNotFound(BaseAPIException):
    """Partner isn't found."""

    message = "Partner not found."
    status_code = status.HTTP_404_NOT_FOUND


__constrains__ = {
    "partners_name_key": PartnerNameAlreadyExists,
    "partners_token_key": PartnerTokenAlreadyExists,
}
