from dataclasses import dataclass
from typing import Tuple

from fastapi import APIRouter, FastAPI

__all__ = ["Routes"]


@dataclass(frozen=True)
class Routes:
    """Frozen model for storage all ``APIRouter``."""

    routers: Tuple[APIRouter, ...]

    def register_routes(self, app: FastAPI):
        """
        Include ``APIRouter`` to the ``FastAPI`` application instance.

        Args:
            app: ``FastAPI`` application instance.

        Examples:
            Usage::

                from routers import users, auth
                __routes__ = Routes(
                    routers=(
                        users.router,
                        auth.router
                    )
                )

        Returns:
            None
        """

        for router in self.routers:
            app.include_router(router)
