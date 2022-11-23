from abc import ABC
from typing import List, TypeVar

from app.pkg.models.base import Model

__all__ = ["Repository", "BaseRepository"]


BaseRepository = TypeVar("BaseRepository", bound="Repository")


class Repository(ABC):
    """Base repository interface."""

    async def create(self, cmd: Model) -> Model:
        raise NotImplementedError

    async def read(self, query: Model) -> Model:
        raise NotImplementedError

    async def read_all(self) -> List[Model]:
        raise NotImplementedError

    async def update(self, cmd: Model) -> Model:
        raise NotImplementedError

    async def delete(self, cmd: Model) -> Model:
        raise NotImplementedError
