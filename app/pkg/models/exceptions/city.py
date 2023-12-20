"""Exceptions for a City model."""

from starlette import status

from app.pkg.models.base import BaseAPIException

__all__ = [
    "CityNotFound",
    "NoCityFoundForCountry",
    "DuplicateCityCode",
    "CountryAlreadyHasCities",
    "CityNameAlreadyExists",
]


class CityNotFound(BaseAPIException):
    message = "City not found."
    status_code = status.HTTP_404_NOT_FOUND


class NoCityFoundForCountry(BaseAPIException):
    message = "City not found for this country."
    status_code = status.HTTP_404_NOT_FOUND


class DuplicateCityCode(BaseAPIException):
    message = "City code already exists."
    status_code = status.HTTP_409_CONFLICT


class CountryAlreadyHasCities(BaseAPIException):
    message = "Country already have this city."
    status_code = status.HTTP_409_CONFLICT


class CityNameAlreadyExists(BaseAPIException):
    message = "City name already exists."
    status_code = status.HTTP_409_CONFLICT


__constrains__ = {
    "cities_code_key": DuplicateCityCode,
    "cities_name_key": CityNameAlreadyExists,
    "unique_country_and_city_code": CountryAlreadyHasCities,
}
