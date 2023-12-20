"""Model for partners.

Aka: Yandex, GeekBrains, etc.
"""
import secrets
import string

from pydantic.fields import Field
from pydantic.types import PositiveInt

from app.pkg.models.base import BaseModel

__all__ = [
    "Partner",
    "CreatePartnerCommand",
    "ReadPartnerQuery",
    "ReadPartnerByTokenQuery",
    "UpdatePartnerCommand",
    "DeletePartnerCommand",
]


class BasePartner(BaseModel):
    """Base model for partners."""


class PartnersFields:
    """Model fields of partners."""

    id: PositiveInt = Field(description="Internal partner id.", example=1)
    name: str = Field(description="Partner name.", example="Yandex")
    token: str = Field(
        description="Partner short token.",
        example="YZVWFclG",
        default_factory=lambda: "".join(
            secrets.choice(string.ascii_letters + string.digits) for _ in range(8)
        ),
    )


class _Partner(BasePartner):
    name: str = PartnersFields.name
    token: str = PartnersFields.token


class Partner(_Partner):
    id: PositiveInt = PartnersFields.id


# Commands.
class CreatePartnerCommand(_Partner):
    ...


class UpdatePartnerCommand(_Partner):
    id: PositiveInt = PartnersFields.id


class DeletePartnerCommand(BasePartner):
    id: PositiveInt = PartnersFields.id


# Queries.
class ReadPartnerQuery(BasePartner):
    id: PositiveInt = PartnersFields.id


class ReadPartnerByTokenQuery(BasePartner):
    token: str = PartnersFields.token
