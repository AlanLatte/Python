"""Module for testing create method of directions repository."""


import pytest

from app.pkg import models
from app.pkg.models.exceptions.direction import DirectionNameAlreadyExists


@pytest.mark.postgresql
async def test_create(
    direction_repository,
    direction_generator,
):
    direction = direction_generator()

    result = await direction_repository.create(
        cmd=direction.migrate(model=models.CreateDirectionCommand),
    )

    assert result == direction.migrate(
        model=models.Direction,
        extra_fields={"id": result.id},
    )


@pytest.mark.postgresql
async def test_create_duplicate(
    direction_repository,
    direction_inserter,
):
    _, cmd = await direction_inserter()

    with pytest.raises(DirectionNameAlreadyExists):
        await direction_repository.create(cmd=cmd)
