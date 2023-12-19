import pytest

from app.internal.repository.postgresql import SkillLevelRepository
from app.pkg import models
from app.pkg.models.exceptions.repository import EmptyResult


@pytest.mark.postgresql
async def test_delete(
    skill_level_repository: SkillLevelRepository,
    skill_level_inserter,
):
    result, cmd = await skill_level_inserter()

    await skill_level_repository.delete(
        cmd=result.migrate(model=models.DeleteSkillLevelCommand)
    )

    with pytest.raises(EmptyResult):
        await skill_level_repository.read(
            query=result.migrate(model=models.ReadSkillLevelQuery)
        )


@pytest.mark.postgresql
async def test_not_found(
    skill_level_repository: SkillLevelRepository, skill_level_generator
):
    cmd = skill_level_generator().migrate(model=models.DeleteSkillLevelCommand)

    with pytest.raises(EmptyResult):
        await skill_level_repository.delete(cmd=cmd)
