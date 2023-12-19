"""Routes for CRUD of contacts."""

from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status
from pydantic.types import SecretStr

from app.internal.pkg.middlewares.token_based_verification import (
    token_based_verification,
)
from app.internal.routes import contacts_router
from app.internal.services import Services
from app.internal.services.contacts import ContactsService
from app.pkg import models
from app.pkg.models.exceptions import contacts


@contacts_router.get(
    "/",
    response_model=List[models.Contacts],
    response_model_exclude={"token", "telegram_user_id"},
    status_code=status.HTTP_200_OK,
    description="Get all contacts",
    dependencies=[Depends(token_based_verification)],
)
@inject
async def read_all_contacts(
    contacts_service: ContactsService = Depends(Provide[Services.contacts_service]),
):
    return await contacts_service.read_all_contacts()


@contacts_router.get(
    "/telegram/{telegram_user_id:int}",
    response_model=models.Contacts,
    response_model_exclude={"telegram_user_id"},
    status_code=status.HTTP_200_OK,
    description="Read specific contacts by telegram user id",
    dependencies=[Depends(token_based_verification)],
)
@inject
async def read_contacts_by_telegram_user_id(
    telegram_user_id: int,
    contacts_service: ContactsService = Depends(Provide[Services.contacts_service]),
):
    return await contacts_service.read_contacts_by_telegram_user_id(
        query=models.ReadContactsByTelegramUserIdQuery(
            telegram_user_id=telegram_user_id,
        ),
    )


@contacts_router.get(
    "/{token:str}",
    response_model=models.Contacts,
    response_model_exclude={"token", "telegram_user_id", "id"},
    status_code=status.HTTP_200_OK,
    description="Read specific contacts",
)
@inject
async def read_contacts_by_token(
    token: SecretStr,
    contacts_service: ContactsService = Depends(Provide[Services.contacts_service]),
):
    return await contacts_service.read_by_token(
        query=models.ReadContactsQuery(token=token),
    )


@contacts_router.post(
    "/",
    response_model=models.Contacts,
    response_model_exclude={"token", "telegram_user_id"},
    status_code=status.HTTP_201_CREATED,
    description="Create contacts",
    dependencies=[Depends(token_based_verification)],
    responses={
        **contacts.ContactsNotFound.generate_openapi(),
        **contacts.TelegramIdAlreadyExists.generate_openapi(),
        **contacts.TelegramUsernameAlreadyExists.generate_openapi(),
        **contacts.TokenAlreadyExists.generate_openapi(),
        **contacts.EmailAlreadyExists.generate_openapi(),
    },
)
@inject
async def create_contacts(
    cmd: models.CreateContactsCommand,
    contacts_service: ContactsService = Depends(Provide[Services.contacts_service]),
):
    return await contacts_service.create_contacts(cmd=cmd)


@contacts_router.put(
    "/{token:str}",
    response_model=models.Contacts,
    response_model_exclude={"token", "telegram_user_id"},
    status_code=status.HTTP_200_OK,
    description="Update contacts",
    responses={
        **contacts.ContactsNotFound.generate_openapi(),
        **contacts.TelegramIdAlreadyExists.generate_openapi(),
        **contacts.TelegramUsernameAlreadyExists.generate_openapi(),
        **contacts.TokenAlreadyExists.generate_openapi(),
        **contacts.EmailAlreadyExists.generate_openapi(),
    },
)
@inject
async def update_contacts(
    token: SecretStr,
    cmd: models.UpdateEmailCommand,
    contacts_service: ContactsService = Depends(Provide[Services.contacts_service]),
):
    return await contacts_service.update_contacts(token=token, cmd=cmd)


@contacts_router.delete(
    "/{contacts_id:int}",
    response_model=models.Contacts,
    response_model_exclude={"token", "telegram_user_id"},
    status_code=status.HTTP_200_OK,
    description="Delete contacts",
    dependencies=[Depends(token_based_verification)],
)
@inject
async def delete_contacts(
    contacts_id: int,
    contacts_service: ContactsService = Depends(Provide[Services.contacts_service]),
):
    return await contacts_service.delete_contacts(
        cmd=models.DeleteContactsCommand(id=contacts_id),
    )
