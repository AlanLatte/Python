import pytest

from app.internal.repository.postgresql import SkillRepository
from app.pkg import models
from app.pkg.models.exceptions.repository import EmptyResult


@pytest.mark.postgresql
async def test_read(skill_repository: SkillRepository, skill_inserter):
    result, cmd = await skill_inserter()

    assert result == await skill_repository.read(
        query=cmd.migrate(model=models.ReadSkillQuery, extra_fields={"id": result.id})
    )


@pytest.mark.postgresql
async def test_not_found(skill_repository: SkillRepository, skill_generator):
    with pytest.raises(EmptyResult):
        await skill_repository.read(
            query=skill_generator().migrate(model=models.ReadSkillQuery)
        )
