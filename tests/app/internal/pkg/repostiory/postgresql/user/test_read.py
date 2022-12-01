import pytest

from app.internal.repository.postgresql import UserRepository
from app.pkg import models
from app.pkg.models.exceptions.repository import EmptyResult


async def test_correct_by_id(
    user_repository: UserRepository, insert_first_user: models.User
):
    user = await user_repository.read(
        query=models.ReadUserByIdQuery(id=insert_first_user.id)
    )
    assert user == insert_first_user


@pytest.mark.parametrize(
    "_id",
    [1, 2, 3],
)
async def test_incorrect_by_id(user_repository: UserRepository, _id: int):
    with pytest.raises(EmptyResult):
        await user_repository.read(query=models.ReadUserByIdQuery(id=_id))
