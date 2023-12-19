"""Module for testing skill creation."""


import asyncio

import pytest

from app.internal.repository.postgresql import SkillRepository
from app.pkg import models
from app.pkg.models.exceptions.skill import SkillNameAlreadyExists


@pytest.mark.postgresql
async def test_create(skill_generator, skill_repository: SkillRepository):
    skill = skill_generator()

    created_skill = await skill_repository.create(
        cmd=skill.migrate(model=models.CreateSkillCommand),
    )

    assert created_skill == skill.migrate(
        model=models.Skill,
        extra_fields={"id": created_skill.id},
    )


@pytest.mark.postgresql
async def test_not_unique_name(skill_generator, skill_repository: SkillRepository):
    skill = skill_generator()

    with pytest.raises(SkillNameAlreadyExists):
        tasks = [
            asyncio.create_task(
                skill_repository.create(
                    cmd=skill.migrate(model=models.CreateSkillCommand),
                ),
            ),
            asyncio.create_task(
                skill_repository.create(
                    cmd=skill.migrate(model=models.CreateSkillCommand),
                ),
            ),
        ]
        await asyncio.gather(*tasks)
