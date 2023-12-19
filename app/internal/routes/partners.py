"""Routes for partners module."""


from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status

from app.internal.pkg.middlewares.token_based_verification import (
    token_based_verification,
)
from app.internal.routes import partners_router
from app.internal.services import Services
from app.internal.services.partners import PartnerService
from app.pkg import models
from app.pkg.models.exceptions import partners


@partners_router.post(
    "/",
    response_model=models.Partner,
    status_code=status.HTTP_201_CREATED,
    description="Create partner",
    dependencies=[Depends(token_based_verification)],
    responses={
        **partners.PartnerTokenAlreadyExists.generate_openapi(),
        **partners.PartnerNameAlreadyExists.generate_openapi(),
    },
)
@inject
async def create_partner(
    cmd: models.CreatePartnerCommand,
    partners_service: PartnerService = Depends(Provide[Services.partner_service]),
):
    return await partners_service.create_partner(cmd=cmd)


@partners_router.get(
    "/{token:str}/",
    response_model=models.Partner,
    status_code=status.HTTP_200_OK,
    description="Read specific partner by token",
)
@inject
async def read_partner_by_token(
    token: str,
    partners_service: PartnerService = Depends(Provide[Services.partner_service]),
):
    return await partners_service.read_partner_by_token(
        query=models.ReadPartnerByTokenQuery(token=token),
    )


@partners_router.get(
    "/",
    response_model=List[models.Partner],
    status_code=status.HTTP_200_OK,
    description="Read all partners",
    dependencies=[Depends(token_based_verification)],
)
@inject
async def read_all_partners(
    partners_service: PartnerService = Depends(Provide[Services.partner_service]),
):
    return await partners_service.read_all_partner()


@partners_router.patch(
    "/",
    response_model=models.Partner,
    status_code=status.HTTP_200_OK,
    description="Update partner",
    dependencies=[Depends(token_based_verification)],
    responses={
        **partners.PartnerTokenAlreadyExists.generate_openapi(),
        **partners.PartnerNameAlreadyExists.generate_openapi(),
    },
)
@inject
async def update_partner(
    cmd: models.UpdatePartnerCommand,
    partners_service: PartnerService = Depends(Provide[Services.partner_service]),
):
    return await partners_service.update_partner(cmd=cmd)


@partners_router.delete(
    "/{partner_id:int}/",
    response_model=models.Partner,
    status_code=status.HTTP_200_OK,
    description="Delete partner",
    dependencies=[Depends(token_based_verification)],
)
@inject
async def delete_partner(
    partner_id: int,
    partners_service: PartnerService = Depends(Provide[Services.partner_service]),
):
    return await partners_service.delete_partner(
        cmd=models.DeletePartnerCommand(id=partner_id),
    )
