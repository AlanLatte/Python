"""Module for testing delete method of skill repository."""


import pytest

from app.internal.repository.postgresql import SkillRepository
from app.pkg import models
from app.pkg.models.exceptions.repository import EmptyResult


@pytest.mark.postgresql
async def test_delete(skill_inserter, skill_repository: SkillRepository):
    skill, _ = await skill_inserter()

    await skill_repository.delete(cmd=skill.migrate(model=models.DeleteSkillCommand))

    with pytest.raises(EmptyResult):
        await skill_repository.read(query=skill.migrate(model=models.ReadSkillQuery))


@pytest.mark.postgresql
async def test_not_found(skill_repository: SkillRepository, skill_generator):
    with pytest.raises(EmptyResult):
        await skill_repository.delete(
            cmd=skill_generator().migrate(model=models.DeleteSkillCommand),
        )
