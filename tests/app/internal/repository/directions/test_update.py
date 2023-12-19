import pytest

from app.internal.repository.postgresql import DirectionRepository
from app.pkg import models
from app.pkg.models.exceptions.repository import EmptyResult
from app.pkg.models.exceptions.direction import DirectionNameAlreadyExists


@pytest.mark.postgresql
async def test_update(
    direction_repository: DirectionRepository, direction_inserter, direction_generator
):
    inserted, _ = await direction_inserter()
    expected = direction_generator(id=inserted.id)
    result = await direction_repository.update(
        cmd=inserted.migrate(
            models.UpdateDirectionCommand,
            extra_fields={"name": expected.name},
        )
    )
    assert result == expected


@pytest.mark.postgresql
async def test_direction_not_found(
    direction_repository: DirectionRepository, direction_inserter
):
    expected, _ = await direction_inserter()
    cmd = expected.migrate(
        models.UpdateDirectionCommand, extra_fields={"id": expected.id + 1}
    )

    with pytest.raises(EmptyResult):
        await direction_repository.update(cmd=cmd)


@pytest.mark.postgresql
async def test_update_duplicate(
    direction_repository: DirectionRepository,
    direction_inserter,
    direction_generator,
):
    inserted, _ = await direction_inserter()
    expected = direction_generator()
    await direction_repository.create(
        cmd=expected.migrate(models.CreateDirectionCommand)
    )
    cmd = inserted.migrate(
        models.UpdateDirectionCommand,
        extra_fields={"name": expected.name},
    )

    with pytest.raises(DirectionNameAlreadyExists):
        await direction_repository.update(cmd=cmd)
