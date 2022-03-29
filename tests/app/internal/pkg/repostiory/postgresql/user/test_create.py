import pytest
from dependency_injector.wiring import inject, Provide

from app.internal.repository.postgresql import Repository, User
from app.pkg import models


@inject
async def test_correct(
    overwrite_connection, repository: User = Provide[Repository.user]
):
    cmd = models.CreateUserCommand(
        email="correct-email@example.ru",
        password="supeR_%$tr0ng-pa$$worD",
        role_name=models.UserRole.USER,
    )
    user = await repository.create(cmd=cmd)
    assert user == models.User(id=user.id, **cmd.to_dict(show_secrets=True))


@pytest.mark.skip(reason="Not implemented")
async def test_incorrect():
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented")
async def test_already_exist():
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented")
async def test_incorrect_email():
    raise NotImplementedError
