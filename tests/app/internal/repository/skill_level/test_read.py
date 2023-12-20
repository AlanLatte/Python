"""Module for testing read skill level repository."""

import pytest

from app.internal.repository.postgresql import SkillLevelRepository
from app.pkg import models
from app.pkg.models.exceptions.repository import EmptyResult


@pytest.mark.postgresql
async def test_read(skill_level_inserter, skill_level_repository: SkillLevelRepository):
    skill_level, _ = await skill_level_inserter()

    result = await skill_level_repository.read(
        query=skill_level.migrate(model=models.ReadSkillLevelQuery),
    )
    assert result == skill_level.migrate(model=models.SkillLevel)


@pytest.mark.postgresql
async def test_not_found(
    skill_level_generator,
    skill_level_repository: SkillLevelRepository,
):
    with pytest.raises(EmptyResult):
        await skill_level_repository.read(
            query=skill_level_generator().migrate(model=models.ReadSkillLevelQuery),
        )
