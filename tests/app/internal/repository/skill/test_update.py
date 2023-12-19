"""Module for testing skill update method."""


import asyncio

import pytest

from app.internal.repository.postgresql import SkillRepository
from app.pkg import models
from app.pkg.models.exceptions.repository import EmptyResult
from app.pkg.models.exceptions.skill import SkillNameAlreadyExists


@pytest.mark.postgresql
async def test_update(skill_inserter, skill_repository: SkillRepository):
    skill, _ = await skill_inserter()

    updated_skill = await skill_repository.update(
        cmd=skill.migrate(
            model=models.UpdateSkillCommand,
            extra_fields={"name": f"{skill.name}_new_name"},
        ),
    )

    assert updated_skill == skill.migrate(
        model=models.Skill,
        extra_fields={"name": f"{skill.name}_new_name"},
    )


@pytest.mark.postgresql
async def test_not_unique_name(skill_inserter, skill_repository: SkillRepository):
    skill, _ = await skill_inserter()
    skill2, _ = await skill_inserter()

    with pytest.raises(SkillNameAlreadyExists):
        tasks = [
            asyncio.create_task(
                skill_repository.update(
                    cmd=skill.migrate(
                        model=models.UpdateSkillCommand,
                        extra_fields={"name": skill2.name},
                    ),
                ),
            ),
            asyncio.create_task(
                skill_repository.update(
                    cmd=skill2.migrate(
                        model=models.UpdateSkillCommand,
                        extra_fields={"name": skill.name},
                    ),
                ),
            ),
        ]
        await asyncio.gather(*tasks)


@pytest.mark.postgresql
async def test_not_found(skill_generator, skill_repository: SkillRepository):
    with pytest.raises(EmptyResult):
        await skill_repository.update(
            cmd=skill_generator().migrate(model=models.UpdateSkillCommand),
        )
