"""Models of student level choicer."""

import typing

from app.internal.repository.postgresql import skill_levels
from app.internal.repository.repository import BaseRepository
from app.pkg import models
from app.pkg.models.exceptions.repository import EmptyResult, UniqueViolation
from app.pkg.models.exceptions.skill_levels import (
    SkillLevelAlreadyExists,
    SkillLevelNotFound,
)

__all__ = ["SkillLevelService"]


class SkillLevelService:
    """Service for manage skill levels."""

    #: SkillLevelRepository: SkillLevelRepository repository implementation.
    repository: skill_levels.SkillLevelRepository

    def __init__(self, skill_level_repository: BaseRepository):
        self.repository = skill_level_repository

    async def create_skill_level(
        self,
        cmd: models.CreateSkillLevelCommand,
    ) -> models.SkillLevel:
        """Create skill level.

        Args:
            cmd: CreateSkillLevelCommand command.

        Returns:
            SkillLevel: Created skill level.
        """
        return await self.repository.create(cmd=cmd)

    async def read_skill_level(
        self,
        query: models.ReadSkillLevelQuery,
    ) -> models.SkillLevel:
        """Read skill level.

        Args:
            query: ReadSkillLevelQuery query.

        Returns:
            SkillLevel: Read skill level.
        """
        return await self.repository.read(query=query)

    async def read_all_skill_levels(self) -> typing.List[models.SkillLevel]:
        """Read all skill levels.

        Returns:
            List[SkillLevel]: Read all skill levels.
        """
        try:
            return await self.repository.read_all()
        except EmptyResult as e:
            raise SkillLevelNotFound from e

    async def update_skill_level(
        self,
        cmd: models.UpdateSkillLevelCommand,
    ) -> models.SkillLevel:
        """Update skill level.

        Args:
            cmd: UpdateSkillLevelCommand command.

        Returns:
            SkillLevel: Updated skill level.
        """
        try:
            return await self.repository.update(cmd=cmd)
        except UniqueViolation as e:
            raise SkillLevelAlreadyExists from e

    async def delete_skill_level(
        self,
        cmd: models.DeleteSkillLevelCommand,
    ) -> models.SkillLevel:
        """Delete skill level.

        Args:
            cmd: DeleteSkillLevelCommand command.

        Returns:
            SkillLevel: Deleted skill level.
        """
        return await self.repository.delete(cmd=cmd)
