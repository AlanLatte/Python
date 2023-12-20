"""Module for testing read_all method in skill_level repository."""


import pytest

from app.internal.repository.postgresql import SkillLevelRepository
from app.pkg.models.exceptions.repository import EmptyResult


@pytest.mark.postgresql
@pytest.mark.slow
async def test_read_all(
    skill_level_inserter,
    skill_level_repository: SkillLevelRepository,
    clean_postgres,
):
    _ = clean_postgres

    skill_level, _ = await skill_level_inserter()

    result = await skill_level_repository.read_all()
    assert result == [skill_level]


@pytest.mark.postgresql
@pytest.mark.slow
async def test_not_found(skill_level_repository: SkillLevelRepository, clean_postgres):
    _ = clean_postgres

    with pytest.raises(EmptyResult):
        await skill_level_repository.read_all()


@pytest.mark.postgresql
@pytest.mark.slow
async def test_multiple_read_all(
    skill_level_inserter,
    skill_level_repository: SkillLevelRepository,
    clean_postgres,
):
    _ = clean_postgres

    skill_level, _ = await skill_level_inserter()
    skill_level2, _ = await skill_level_inserter()

    result = await skill_level_repository.read_all()
    assert result == [skill_level, skill_level2]
