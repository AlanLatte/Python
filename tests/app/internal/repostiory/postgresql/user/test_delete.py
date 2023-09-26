"""Test cases for :meth:`.UserRepository.delete()`."""

import pytest

from app.internal.repository.postgresql import UserRepository
from app.pkg import models
from app.pkg.models.exceptions.repository import EmptyResult


async def test_correct(user_repository: UserRepository, insert_first_user: models.User):
    user = await user_repository.delete(
        cmd=models.DeleteUserCommand(id=insert_first_user.id),
    )
    assert insert_first_user == user


@pytest.mark.parametrize(
    "user_id",
    [1, 2, 3, 4],
)
async def test_incorrect_user_id_not_found(
    user_repository: UserRepository,
    user_id: int,
):
    with pytest.raises(EmptyResult):
        await user_repository.delete(cmd=models.DeleteUserCommand(id=user_id))
