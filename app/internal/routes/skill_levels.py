"""Routers for CRUD of skill levels."""

from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status

from app.internal.pkg.middlewares.token_based_verification import (
    token_based_verification,
)
from app.internal.routes import skill_levels_router
from app.internal.services import Services
from app.internal.services.skill_levels import SkillLevelService
from app.pkg import models


@skill_levels_router.get(
    "/",
    response_model=List[models.SkillLevel],
    status_code=status.HTTP_200_OK,
    description="Get all skill levels",
)
@inject
async def read_all_skill_levels(
    skill_level_service: SkillLevelService = Depends(
        Provide[Services.skill_levels_service],
    ),
):
    return await skill_level_service.read_all_skill_levels()


@skill_levels_router.get(
    "/{skill_level_id:int}/",
    response_model=models.SkillLevel,
    status_code=status.HTTP_200_OK,
    description="Read specific skill level",
    dependencies=[Depends(token_based_verification)],
)
@inject
async def read_skill_level(
    skill_level_id: int,
    skill_level_service: SkillLevelService = Depends(
        Provide[Services.skill_levels_service],
    ),
):
    return await skill_level_service.read_skill_level(
        query=models.ReadSkillLevelQuery(id=skill_level_id),
    )


@skill_levels_router.post(
    "/",
    response_model=models.SkillLevel,
    status_code=status.HTTP_201_CREATED,
    description="Create skill level",
    dependencies=[Depends(token_based_verification)],
)
@inject
async def create_skill_level(
    cmd: models.CreateSkillLevelCommand,
    skill_level_service: SkillLevelService = Depends(
        Provide[Services.skill_levels_service],
    ),
):
    return await skill_level_service.create_skill_level(cmd=cmd)


@skill_levels_router.put(
    "/",
    response_model=models.SkillLevel,
    status_code=status.HTTP_200_OK,
    description="Update skill level",
    dependencies=[Depends(token_based_verification)],
)
@inject
async def update_skill_level(
    cmd: models.UpdateSkillLevelCommand,
    skill_level_service: SkillLevelService = Depends(
        Provide[Services.skill_levels_service],
    ),
):
    return await skill_level_service.update_skill_level(cmd=cmd)


@skill_levels_router.delete(
    "/{skill_level_id:int}",
    response_model=models.SkillLevel,
    status_code=status.HTTP_200_OK,
    description="Delete specific skill level",
    dependencies=[Depends(token_based_verification)],
)
@inject
async def delete_skill_level(
    skill_level_id: int,
    skill_level_service: SkillLevelService = Depends(
        Provide[Services.skill_levels_service],
    ),
):
    return await skill_level_service.delete_skill_level(
        cmd=models.DeleteSkillLevelCommand(id=skill_level_id),
    )
