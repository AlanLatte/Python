"""Routers for CRUD of countries."""

from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status

from app.internal.pkg.middlewares.token_based_verification import (
    token_based_verification,
)
from app.internal.routes import country_router
from app.internal.services import Services
from app.internal.services.country import CountryService
from app.pkg import models


@country_router.get(
    "/",
    response_model=List[models.Country],
    status_code=status.HTTP_200_OK,
    description="Get all country",
)
@inject
async def read_all_country(
    country_service: CountryService = Depends(Provide[Services.country_service]),
):
    return await country_service.read_all_countries()


@country_router.get(
    "/{country_id:int}/",
    response_model=models.Country,
    status_code=status.HTTP_200_OK,
    description="Read specific country",
    dependencies=[Depends(token_based_verification)],
)
@inject
async def read_country(
    country_id: int,
    country_service: CountryService = Depends(Provide[Services.country_service]),
):
    return await country_service.read_country(
        query=models.ReadCountryQuery(id=country_id),
    )


@country_router.post(
    "/",
    response_model=models.Country,
    status_code=status.HTTP_201_CREATED,
    description="Create country",
    dependencies=[Depends(token_based_verification)],
)
@inject
async def create_country(
    cmd: models.CreateCountryCommand,
    country_service: CountryService = Depends(Provide[Services.country_service]),
):
    return await country_service.create_country(cmd=cmd)


@country_router.put(
    "/",
    response_model=models.Country,
    status_code=status.HTTP_200_OK,
    description="Update country",
    dependencies=[Depends(token_based_verification)],
)
@inject
async def update_country(
    cmd: models.UpdateCountryCommand,
    country_service: CountryService = Depends(Provide[Services.country_service]),
):
    return await country_service.update_country(cmd=cmd)


@country_router.delete(
    "/{country_id:int}/",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete country",
    dependencies=[Depends(token_based_verification)],
)
@inject
async def delete_country(
    country_id: int,
    country_service: CountryService = Depends(Provide[Services.country_service]),
):
    return await country_service.delete_country(
        cmd=models.DeleteCountryCommand(id=country_id),
    )
