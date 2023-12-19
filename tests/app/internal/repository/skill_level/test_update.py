"""Module for testing update method of skill level repository."""


import pytest

from app.internal.repository.postgresql import SkillLevelRepository
from app.pkg import models
from app.pkg.models.exceptions.repository import EmptyResult
from app.pkg.models.exceptions.skill_levels import SkillLevelAlreadyExists


@pytest.mark.postgresql
async def test_update(
    skill_level_repository: SkillLevelRepository,
    skill_level_inserter,
    skill_level_generator,
):
    result, cmd = await skill_level_inserter()
    cmd = skill_level_generator().migrate(
        model=models.UpdateSkillLevelCommand,
        extra_fields={"id": result.id},
    )

    after_update = await skill_level_repository.update(cmd=cmd)
    assert after_update == cmd.migrate(
        model=models.SkillLevel,
        extra_fields={"id": result.id},
    )


@pytest.mark.postgresql
async def test_not_found(
    skill_level_repository: SkillLevelRepository,
    skill_level_generator,
):
    cmd = skill_level_generator().migrate(model=models.UpdateSkillLevelCommand)

    with pytest.raises(EmptyResult):
        await skill_level_repository.update(cmd=cmd)


@pytest.mark.postgresql
async def test_level_not_unique(
    skill_level_repository: SkillLevelRepository,
    skill_level_inserter,
):
    _, cmd = await skill_level_inserter()
    result, _ = await skill_level_inserter()

    with pytest.raises(SkillLevelAlreadyExists):
        await skill_level_repository.update(
            cmd=cmd.migrate(
                model=models.UpdateSkillLevelCommand,
                extra_fields={"id": result.id},
            ),
        )
