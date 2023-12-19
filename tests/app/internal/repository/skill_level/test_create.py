import pytest

from app.internal.repository.postgresql import SkillLevelRepository
from app.pkg import models
from app.pkg.models.exceptions.skill_levels import SkillLevelAlreadyExists


@pytest.mark.postgresql
async def test_create(
    skill_level_repository: SkillLevelRepository, skill_level_generator
):
    cmd = skill_level_generator().migrate(model=models.CreateSkillLevelCommand)
    result = await skill_level_repository.create(cmd=cmd)

    assert result == cmd.migrate(
        model=models.SkillLevel, extra_fields={"id": result.id}
    )


@pytest.mark.postgresql
async def test_level_not_unique(
    skill_level_repository: SkillLevelRepository, skill_level_inserter
):
    skill_level, cmd = await skill_level_inserter()

    with pytest.raises(SkillLevelAlreadyExists):
        await skill_level_repository.create(
            cmd=skill_level.migrate(model=models.CreateSkillLevelCommand)
        )
