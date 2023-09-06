"""Migration methods."""

import asyncio
from argparse import ArgumentParser

from dependency_injector.wiring import Provide, inject
from yoyo import get_backend, read_migrations

from app.configuration import __containers__
from app.internal.services import Services, UserService
from app.internal.services.user_roles import UserRoleService
from app.pkg import models
from app.pkg.connectors import PostgresSQL
from app.pkg.models.base import BaseAPIException
from app.pkg.models.exceptions.repository import EmptyResult
from app.pkg.settings import settings


def _apply(backend, migrations):
    """Apply all migrations from `migrations`."""
    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))


def _rollback(backend, migrations):
    """Rollback all migrations."""
    with backend.lock():
        backend.rollback_migrations(backend.to_rollback(migrations))


def _rollback_one(backend, migrations):
    """Rollback one migration."""
    with backend.lock():
        migrations = backend.to_rollback(migrations)
        for migration in migrations:
            backend.rollback_one(migration)
            break


def _reload(backend, migrations):
    """Rollback all and apply all migrations."""
    with backend.lock():
        backend.rollback_migrations(backend.to_rollback(migrations))
        backend.apply_migrations(backend.to_apply(migrations))


@inject
async def insert_default_user(
    user_service: UserService = Provide[Services.user_service],
) -> models.User:
    try:
        user = await user_service.read_specific_user_by_username(
            query=models.ReadUserByUserNameQuery(
                username=settings.API.DEFAULT_USER.USERNAME
            )
        )
    except EmptyResult:
        user = await user_service.create_user(
            cmd=models.CreateUserCommand(
                username=settings.API.DEFAULT_USER.USERNAME,
                password=settings.API.DEFAULT_USER.PASSWORD.get_secret_value(),
                role_name=settings.API.DEFAULT_USER.ROLE,
            )
        )

    return user


@inject
async def insert_roles(
    user_role_service: UserRoleService = Provide[Services.user_role_service],
) -> None:
    async for role in user_role_service.create_all_user_roles():
        if isinstance(role, BaseAPIException):
            print(f"ERROR ON INSERT: {role}")


async def inserter() -> None:
    """Function for pre-insert data before running main application instance"""
    await insert_roles()

    inserters = [
        insert_default_user(),
    ]

    await asyncio.gather(*inserters)


@inject
def run(
    action,
):
    """Run ``yoyo-migrations`` based on cli_arguments.

    Notes:
        Before running backend migrations, `run` wiring injections.

    Args:
        action(Callable[..., None]): Target function.

    Returns:
        None
    """

    backend = get_backend(settings.POSTGRES.DSN)
    migrations = read_migrations("migrations")
    action(backend, migrations)


def parse_cli_args():
    """Parse cli arguments."""

    parser = ArgumentParser(description="Apply migrations")
    parser.add_argument("--rollback", action="store_true", help="Rollback migrations")
    parser.add_argument(
        "--rollback-one",
        action="store_true",
        help="Rollback one migration",
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Rollback all migration and applying again",
    )
    parser.add_argument(
        "--testing",
        action="store_true",
        help="Rollback all migration and applying again",
    )
    args = parser.parse_args()

    return args


def cli():
    """Dispatch function, based on cli arguments."""

    args = parse_cli_args()

    if args.rollback:
        action = _rollback
    elif args.rollback_one:
        action = _rollback_one
    elif args.reload:
        action = _reload
    else:
        action = _apply

    __containers__.set_environment(
        connectors=[PostgresSQL], testing=args.testing, pkg_name=__name__
    )
    run(action)

    if args.testing:
        run(action)

    if not (args.rollback or args.rollback_one) or not args:
        asyncio.run(inserter())


if __name__ == "__main__":
    cli()
