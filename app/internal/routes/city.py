"""Routes for city module."""


from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status

from app.internal.pkg.middlewares.token_based_verification import (
    token_based_verification,
)
from app.internal.routes import city_router
from app.internal.services import Services
from app.internal.services.city import CityService
from app.pkg import models


@city_router.get(
    "/",
    response_model=List[models.City],
    status_code=status.HTTP_200_OK,
    description="Get all city",
    dependencies=[Depends(token_based_verification)],
)
@inject
async def read_all_city(
    city_service: CityService = Depends(Provide[Services.city_service]),
):
    return await city_service.read_all_cities()


@city_router.get(
    "/{country_id:int}/",
    response_model=List[models.City],
    status_code=status.HTTP_200_OK,
    description="Read specific city",
)
@inject
async def read_city_by_country(
    country_id: int,
    city_service: CityService = Depends(Provide[Services.city_service]),
):
    return await city_service.read_cities_by_country(
        query=models.ReadCityByCountryQuery(country_id=country_id),
    )


@city_router.post(
    "/",
    response_model=models.City,
    status_code=status.HTTP_201_CREATED,
    description="Create city",
    dependencies=[Depends(token_based_verification)],
)
@inject
async def create_city(
    cmd: models.CreateCityCommand,
    city_service: CityService = Depends(Provide[Services.city_service]),
):
    return await city_service.create_city(cmd=cmd)


@city_router.put(
    "/",
    response_model=models.City,
    status_code=status.HTTP_200_OK,
    description="Update city",
    dependencies=[Depends(token_based_verification)],
)
@inject
async def update_city(
    cmd: models.UpdateCityCommand,
    city_service: CityService = Depends(Provide[Services.city_service]),
):
    return await city_service.update_city(cmd=cmd)


@city_router.delete(
    "/{city_id:int}/",
    response_model=models.City,
    status_code=status.HTTP_200_OK,
    description="Delete city",
    dependencies=[Depends(token_based_verification)],
)
@inject
async def delete_city(
    city_id: int,
    city_service: CityService = Depends(Provide[Services.city_service]),
):
    return await city_service.delete_city(cmd=models.DeleteCityCommand(id=city_id))
