"""Module for testing delete method of direction repository."""

import pytest

from app.internal.repository.postgresql import DirectionRepository
from app.pkg import models
from app.pkg.models.exceptions.repository import EmptyResult


@pytest.mark.postgresql
async def test_delete(direction_repository: DirectionRepository, direction_inserter):
    expected, _ = await direction_inserter()

    await direction_repository.delete(cmd=models.DeleteDirectionCommand(id=expected.id))

    with pytest.raises(EmptyResult):
        await direction_repository.read(query=models.ReadDirectionQuery(id=expected.id))


@pytest.mark.postgresql
async def test_direction_not_found(
    direction_repository: DirectionRepository,
    direction_inserter,
):
    expected, _ = await direction_inserter()
    cmd = expected.migrate(
        models.DeleteDirectionCommand,
        extra_fields={"id": expected.id + 1},
    )

    with pytest.raises(EmptyResult):
        await direction_repository.delete(cmd=cmd)
