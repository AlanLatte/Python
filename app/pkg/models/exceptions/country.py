"""Exceptions for a Country model."""

from starlette import status

from app.pkg.models.base import BaseAPIException

__all__ = ["CountryNameAlreadyExists", "CountryCodeAlreadyExists", "CountryNotFound"]


class CountryNameAlreadyExists(BaseAPIException):
    message = "This 'name' of country already exists."
    status_code = status.HTTP_409_CONFLICT


class CountryCodeAlreadyExists(BaseAPIException):
    message = "This 'code' of country already exists."
    status_code = status.HTTP_409_CONFLICT


class CountryNotFound(BaseAPIException):
    message = "Country not found."
    status_code = status.HTTP_404_NOT_FOUND


__constrains__ = {
    "cities_country_id_fkey": CountryNotFound,
    "countries_name_key": CountryNameAlreadyExists,
    "countries_code_key": CountryCodeAlreadyExists,
}
