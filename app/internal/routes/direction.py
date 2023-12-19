"""Routes for direction module."""

from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status

from app.internal.pkg.middlewares.token_based_verification import (
    token_based_verification,
)
from app.internal.routes import direction_router
from app.internal.services import Services
from app.internal.services.direction import DirectionService
from app.pkg import models


@direction_router.get(
    "/",
    response_model=List[models.Direction],
    status_code=status.HTTP_200_OK,
    description="Get all directions",
)
@inject
async def read_all_directions(
    direction_service: DirectionService = Depends(Provide[Services.direction_service]),
):
    return await direction_service.read_all_directions()


@direction_router.get(
    "/{direction_id:int}/",
    response_model=models.Direction,
    status_code=status.HTTP_200_OK,
    description="Read specific direction",
    dependencies=[Depends(token_based_verification)],
)
@inject
async def read_direction(
    direction_id: int,
    direction_service: DirectionService = Depends(Provide[Services.direction_service]),
):
    return await direction_service.read_direction(
        query=models.ReadDirectionQuery(id=direction_id),
    )


@direction_router.post(
    "/",
    response_model=models.Direction,
    status_code=status.HTTP_201_CREATED,
    description="Create direction",
    dependencies=[Depends(token_based_verification)],
)
@inject
async def create_direction(
    cmd: models.CreateDirectionCommand,
    direction_service: DirectionService = Depends(Provide[Services.direction_service]),
):
    return await direction_service.create_direction(cmd=cmd)


@direction_router.put(
    "/",
    response_model=models.Direction,
    status_code=status.HTTP_200_OK,
    description="Update direction",
    dependencies=[Depends(token_based_verification)],
)
@inject
async def update_direction(
    cmd: models.UpdateDirectionCommand,
    direction_service: DirectionService = Depends(Provide[Services.direction_service]),
):
    return await direction_service.update_direction(cmd=cmd)


@direction_router.delete(
    "/{direction_id:int}/",
    response_model=models.Direction,
    status_code=status.HTTP_200_OK,
    description="Delete direction",
    dependencies=[Depends(token_based_verification)],
)
@inject
async def delete_direction(
    direction_id: int,
    direction_service: DirectionService = Depends(Provide[Services.direction_service]),
):
    return await direction_service.delete_direction(
        cmd=models.DeleteDirectionCommand(id=direction_id),
    )
