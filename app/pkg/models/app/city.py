"""Models of city object."""

from pydantic.fields import Field
from pydantic.types import PositiveInt

from app.pkg.models.base import BaseModel

__all__ = [
    "City",
    "CreateCityCommand",
    "ReadCityQuery",
    "ReadCityByCountryQuery",
    "UpdateCityCommand",
    "DeleteCityCommand",
]


class BaseCity(BaseModel):
    """Base model for city."""


class CityFields:
    id: PositiveInt = Field(description="Internal skill id.", example=1)
    name: PositiveInt = Field(description="City name.", example="Moscow")
    code: str = Field(description="City code.", example="MSK", regex=r"^[A-Z]{3}$")
    country_id: PositiveInt = Field(description="Country id.", example=1)


class _City(BaseCity):
    name: str = CityFields.name
    code: str = CityFields.code
    country_id: PositiveInt = CityFields.country_id


class City(_City):
    id: PositiveInt = CityFields.id


# Commands.
class CreateCityCommand(_City):
    ...


class UpdateCityCommand(_City):
    id: PositiveInt = CityFields.id


class DeleteCityCommand(BaseCity):
    id: PositiveInt = CityFields.id


# Queries.
class ReadCityQuery(BaseCity):
    id: PositiveInt = CityFields.id


class ReadCityByCountryQuery(BaseCity):
    country_id: PositiveInt = CityFields.country_id
