from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Security, status

from app.internal.services import Services
from app.internal.services.user import UserService
from app.pkg import models
from app.pkg.jwt import JwtAuthorizationCredentials, access_security

router = APIRouter(prefix="/user", tags=["User"])


@router.post(
    "/",
    response_model=models.User,
    status_code=status.HTTP_201_CREATED,
    description="Create user",
    response_model_exclude={"password"},
)
@inject
async def create_user(
    cmd: models.CreateUserCommand,
    user_service: UserService = Depends(Provide[Services.user_service]),
    _: JwtAuthorizationCredentials = Security(access_security),
):
    return await user_service.create_user(cmd=cmd)


@router.get(
    "/",
    response_model=List[models.User],
    status_code=status.HTTP_200_OK,
    response_model_exclude={"password"},
    description="Get all users without password field",
)
@inject
async def read_all_users(
    user_service: UserService = Depends(Provide[Services.user_service]),
    _: JwtAuthorizationCredentials = Security(access_security),
):
    return await user_service.read_all_users()


@router.get(
    "/{user_id:int}",
    response_model=models.User,
    status_code=status.HTTP_200_OK,
    response_model_exclude={"password"},
    description="Read specific user without password field",
)
@inject
async def read_user(
    user_id: int,
    user_service: UserService = Depends(Provide[Services.user_service]),
    _: JwtAuthorizationCredentials = Security(access_security),
):
    return await user_service.read_specific_user_by_id(
        query=models.ReadUserByIdQuery(id=user_id),
    )


@router.delete(
    "/{user_id:int}",
    response_model=List[models.User],
    status_code=status.HTTP_200_OK,
    response_model_exclude={"password"},
    description="Delete specific user",
)
@inject
async def delete_user(
    user_id: int,
    user_service: UserService = Depends(Provide[Services.user_service]),
    _: JwtAuthorizationCredentials = Security(access_security),
):
    return await user_service.delete_specific_user(
        cmd=models.DeleteUserCommand(id=user_id),
    )
