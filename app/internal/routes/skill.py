"""Routes for skill module."""

from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status

from app.internal.pkg.middlewares.token_based_verification import (
    token_based_verification,
)
from app.internal.routes import skill_router
from app.internal.services import Services
from app.internal.services.skill import SkillService
from app.pkg import models


@skill_router.get(
    "/",
    response_model=List[models.Skill],
    status_code=status.HTTP_200_OK,
    description="Get all skills",
)
@inject
async def read_all_skills(
    skill_service: SkillService = Depends(Provide[Services.skill_service]),
):
    return await skill_service.read_all_skills()


@skill_router.get(
    "/{skill_id:int}/",
    response_model=models.Skill,
    status_code=status.HTTP_200_OK,
    description="Read specific skill",
    dependencies=[Depends(token_based_verification)],
)
@inject
async def read_skill(
    skill_id: int,
    skill_service: SkillService = Depends(Provide[Services.skill_service]),
):
    return await skill_service.read_skill(
        query=models.ReadSkillQuery(id=skill_id),
    )


@skill_router.post(
    "/",
    response_model=models.Skill,
    status_code=status.HTTP_201_CREATED,
    description="Create skill",
    dependencies=[Depends(token_based_verification)],
)
@inject
async def create_skill(
    cmd: models.CreateSkillCommand,
    skill_service: SkillService = Depends(Provide[Services.skill_service]),
):
    return await skill_service.create_skill(cmd=cmd)


@skill_router.put(
    "/",
    response_model=models.Skill,
    status_code=status.HTTP_200_OK,
    description="Update skill",
    dependencies=[Depends(token_based_verification)],
)
@inject
async def update_skill(
    cmd: models.UpdateSkillCommand,
    skill_service: SkillService = Depends(Provide[Services.skill_service]),
):
    return await skill_service.update_skill(cmd=cmd)


@skill_router.delete(
    "/{skill_id:int}/",
    response_model=models.Skill,
    status_code=status.HTTP_200_OK,
    description="Delete skill",
    dependencies=[Depends(token_based_verification)],
)
@inject
async def delete_skill(
    skill_id: int,
    skill_service: SkillService = Depends(Provide[Services.skill_service]),
):
    return await skill_service.delete_skill(cmd=models.DeleteSkillCommand(id=skill_id))
