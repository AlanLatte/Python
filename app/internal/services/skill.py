"""Service for manage student skills."""


import typing

from app.internal.repository.postgresql import skill
from app.internal.repository.repository import BaseRepository
from app.pkg import models
from app.pkg.models.exceptions.repository import EmptyResult, UniqueViolation
from app.pkg.models.exceptions.skill import SkillNameAlreadyExists, SkillNotFound

__all__ = ["SkillService"]


class SkillService:
    """Service for manage skills."""

    #: SkillRepository: SkillRepository repository implementation.
    repository: skill.SkillRepository

    def __init__(self, skill_repository: BaseRepository):
        self.repository = skill_repository

    async def create_skill(self, cmd: models.CreateSkillCommand) -> models.Skill:
        """Create skill.

        Args:
            cmd: CreateSkillCommand command.

        Returns:
            Skill: Created skill.
        """
        try:
            return await self.repository.create(cmd=cmd)
        except UniqueViolation as e:
            raise SkillNameAlreadyExists from e

    async def read_skill(self, query: models.ReadSkillQuery) -> models.Skill:
        """Read skill.

        Args:
            query: ReadSkillQuery query.

        Returns:
            Skill: Read skill.
        """
        try:
            return await self.repository.read(query=query)
        except EmptyResult as e:
            raise SkillNotFound from e

    async def batch_read_all_skills(
        self,
        query: models.ReadAllSkillByIdQuery,
    ) -> typing.List[models.Skill]:
        """Read all skills by ids.

        Args:
            query: ReadAllSkillByIdQuery command.

        Returns:
            List[Skill]: Read all skills by ids.
        """
        try:
            return await self.repository.batch_read_all(query=query)
        except EmptyResult as e:
            raise SkillNotFound from e

    async def read_all_skills(self) -> typing.List[models.Skill]:
        """Read all skills.

        Returns:
            List[Skill]: Read all skills.
        """
        return await self.repository.read_all()

    async def update_skill(self, cmd: models.UpdateSkillCommand) -> models.Skill:
        """Update skill.

        Args:
            cmd: UpdateSkillCommand command.

        Returns:
            Skill: Updated skill.
        """
        return await self.repository.update(cmd=cmd)

    async def delete_skill(self, cmd: models.DeleteSkillCommand) -> None:
        """Delete skill.

        Args:
            cmd: DeleteSkillCommand command.
        """
        return await self.repository.delete(cmd=cmd)
