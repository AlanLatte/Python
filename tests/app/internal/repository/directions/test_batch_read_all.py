import pytest

from app.internal.repository.postgresql import DirectionRepository
from app.pkg import models
from app.pkg.models.exceptions.repository import EmptyResult


@pytest.mark.postgresql
async def test_batch_read_all(
    direction_repository: DirectionRepository,
    direction_inserter,
    check_array_equality,
):
    expected = []
    cmds = []
    for _ in range(10):
        result, cmd = await direction_inserter()
        expected.append(result)
        cmds.append(cmd)

    query = models.ReadAllDirectionByIdQuery(ids=list(map(lambda x: x.id, expected)))

    result = await direction_repository.batch_read_all(query=query)

    assert check_array_equality(expected, result)


@pytest.mark.postgresql
async def test_empty(
    direction_repository: DirectionRepository,
):
    query = models.ReadAllDirectionByIdQuery(ids=[])
    with pytest.raises(EmptyResult):
        await direction_repository.batch_read_all(query=query)


@pytest.mark.postgresql
async def test_not_found(
    direction_repository: DirectionRepository,
    direction_inserter,
):
    expected, _ = await direction_inserter()
    query = expected.migrate(
        models.ReadAllDirectionByIdQuery, extra_fields={"ids": [expected.id + 1]}
    )

    with pytest.raises(EmptyResult):
        await direction_repository.batch_read_all(query=query)


@pytest.mark.postgresql
async def test_duplicate(
    direction_repository: DirectionRepository, direction_inserter, check_array_equality
):
    expected, _ = await direction_inserter()
    query = expected.migrate(
        models.ReadAllDirectionByIdQuery,
        extra_fields={"ids": [expected.id, expected.id]},
    )

    actual = await direction_repository.batch_read_all(query=query)

    assert check_array_equality([expected], actual)


@pytest.mark.postgresql
async def test_one_of_ids_incorrect(
    direction_repository: DirectionRepository, direction_inserter, check_array_equality
):
    expected, _ = await direction_inserter()
    query = expected.migrate(
        models.ReadAllDirectionByIdQuery,
        extra_fields={"ids": [expected.id, expected.id + 1]},
    )

    actual = await direction_repository.batch_read_all(query=query)

    assert check_array_equality([expected], actual)
