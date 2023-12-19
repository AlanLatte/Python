"""Module for testing read_all method."""


import pytest

from app.internal.repository.postgresql import SkillRepository
from app.pkg.models.exceptions.repository import EmptyResult


@pytest.mark.postgresql
@pytest.mark.slow
async def test_read_all(
    skill_repository: SkillRepository,
    skill_inserter,
    clean_postgres,
):
    _ = clean_postgres

    expected = []
    cmds = []
    for _ in range(10):
        result, cmd = await skill_inserter()
        expected.append(result)
        cmds.append(cmd)

    result = await skill_repository.read_all()

    assert result == expected


@pytest.mark.postgresql
@pytest.mark.slow
async def test_empty(skill_repository: SkillRepository, clean_postgres):
    _ = clean_postgres

    with pytest.raises(EmptyResult):
        await skill_repository.read_all()
