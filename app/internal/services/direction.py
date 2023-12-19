"""Service for manage directions."""


import typing

from app.internal.repository.postgresql import direction
from app.internal.repository.repository import BaseRepository
from app.pkg import models
from app.pkg.models.exceptions.direction import (
    DirectionNameAlreadyExists,
    DirectionNotFound,
)
from app.pkg.models.exceptions.repository import EmptyResult, UniqueViolation

__all__ = ["DirectionService"]


class DirectionService:
    """Service for manage directions."""

    #: DirectionRepository: DirectionRepository repository implementation.
    repository: direction.DirectionRepository

    def __init__(self, direction_repository: BaseRepository):
        self.repository = direction_repository

    async def create_direction(
        self,
        cmd: models.CreateDirectionCommand,
    ) -> models.Direction:
        """Create direction.

        Args:
            cmd: CreateDirectionCommand command.

        Returns:
            Direction: Created direction.
        """
        try:
            return await self.repository.create(cmd=cmd)
        except UniqueViolation as e:
            raise DirectionNameAlreadyExists from e

    async def read_direction(
        self,
        query: models.ReadDirectionQuery,
    ) -> models.Direction:
        """Read direction.

        Args:
            query: ReadDirectionQuery query.

        Returns:
            Direction: Read direction.
        """
        return await self.repository.read(query=query)

    async def read_all_direction_by_ids(
        self,
        query: models.ReadAllDirectionByIdQuery,
    ) -> typing.List[models.Direction]:
        """Read all directions by ids.

        Args:
            query: ReadAllDirectionByIdQuery command.

        Returns:
            List[Direction]: Read all directions by ids.
        """
        try:
            return await self.repository.batch_read_all(query=query)
        except EmptyResult as e:
            raise DirectionNotFound from e

    async def read_all_directions(self) -> typing.List[models.Direction]:
        """Read all directions.

        Returns:
            List[Direction]: Read all directions.
        """
        try:
            return await self.repository.read_all()
        except EmptyResult as e:
            raise DirectionNotFound from e

    async def update_direction(
        self,
        cmd: models.UpdateDirectionCommand,
    ) -> models.Direction:
        """Update direction.

        Args:
            cmd: UpdateDirectionCommand command.

        Returns:
            Direction: Updated direction.
        """
        return await self.repository.update(cmd=cmd)

    async def delete_direction(
        self,
        cmd: models.DeleteDirectionCommand,
    ) -> models.Direction:
        """Delete direction.

        Args:
            cmd: DeleteDirectionCommand command.

        Returns:
            Direction: Deleted direction.
        """
        return await self.repository.delete(cmd=cmd)
