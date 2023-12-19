import pytest

from app.pkg import models
from app.pkg.models.exceptions.repository import EmptyResult
from app.internal.repository.postgresql import SkillRepository


@pytest.mark.postgresql
async def test_batch_read_all(
    skill_repository: SkillRepository, skill_inserter, check_array_equality
):
    expected = []
    cmds = []
    for _ in range(10):
        result, cmd = await skill_inserter()
        expected.append(result)
        cmds.append(cmd)

    query = models.ReadAllSkillByIdQuery(ids=list(map(lambda x: x.id, expected)))

    result = await skill_repository.batch_read_all(query=query)

    assert check_array_equality(expected, result)


@pytest.mark.postgresql
async def test_empty(
    skill_repository: SkillRepository,
):
    query = models.ReadAllSkillByIdQuery(ids=[])
    with pytest.raises(EmptyResult):
        await skill_repository.batch_read_all(query=query)
