"""Service for manage partners."""
import typing

from app.internal.repository.postgresql import partners
from app.internal.repository.repository import BaseRepository
from app.pkg import models
from app.pkg.models.exceptions.partners import PartnerNameAlreadyExists, PartnerNotFound
from app.pkg.models.exceptions.repository import EmptyResult, UniqueViolation

__all__ = ["PartnerService"]


class PartnerService:
    """Service for manage partners."""

    #: PartnerRepository: PartnerRepository repository implementation.
    repository: partners.PartnerRepository

    def __init__(self, partner_repository: BaseRepository):
        self.repository = partner_repository

    async def create_partner(
        self,
        cmd: models.CreatePartnerCommand,
    ) -> models.Partner:
        """Create partner.

        Args:
            cmd: CreatePartnerCommand command.

        Returns:
            Partner: Created partners.
        """
        try:
            return await self.repository.create(cmd=cmd)
        except UniqueViolation as e:
            raise PartnerNameAlreadyExists from e

    async def read_partner(self, query: models.ReadPartnerQuery) -> models.Partner:
        """Read partners.

        Args:
            query: ReadPartnerQuery query.

        Returns:
            Partner: Read partners.
        """
        try:
            return await self.repository.read(query=query)
        except EmptyResult as e:
            raise PartnerNotFound from e

    async def read_partner_by_token(
        self,
        query: models.ReadPartnerByTokenQuery,
    ) -> models.Partner:
        """Read partners.

        Args:
            query: ReadPartnerQuery query.

        Returns:
            Partner: Read partners.
        """
        try:
            return await self.repository.read_by_token(query=query)
        except EmptyResult as e:
            raise PartnerNotFound from e

    async def read_all_partner(
        self,
    ) -> typing.List[models.Partner]:
        """Read all partners.

        Returns:
            typing.List[Partner]: Read partners.
        """
        return await self.repository.read_all()

    async def update_partner(
        self,
        cmd: models.UpdatePartnerCommand,
    ) -> models.Partner:
        """Update partners.

        Args:
            cmd: UpdatePartnerCommand command.

        Returns:
            Partner: Updated partners.
        """
        return await self.repository.update(cmd=cmd)

    async def delete_partner(
        self,
        cmd: models.DeletePartnerCommand,
    ) -> models.Partner:
        """Delete partners.

        Args:
            cmd: DeletePartnerCommand command.

        Returns:
            Partner: Deleted partners.
        """
        return await self.repository.delete(cmd=cmd)
