"""Model for contain ``APIRouter`` instance."""

from dataclasses import dataclass
from typing import Tuple

from fastapi import APIRouter, FastAPI

__all__ = ["Routes"]


@dataclass(frozen=True)
class Routes:
    """Frozen model for storage all ``APIRouter``."""

    routers: Tuple[APIRouter, ...]

    def register_routes(self, app: FastAPI):
        """Include ``APIRouter`` to the ``FastAPI`` application instance.

        Args:
            app: ``FastAPI`` application instance.

        Examples:
            For register routes, you **must** provide routers to model.::

                from routers import users, auth
                __routes__ = Routes(
                    routers=(
                        users.router,
                        auth.router
                    )
                )

            If you call ``register_routes``, all routes from *self.routers* will be
            included to the ``FastAPI`` instance.::

                from fastapi import FastAPI

                app = FastAPI()
                __routes__.register_routes(app=app)

        Returns:
            None
        """

        for router in self.routers:
            app.include_router(router)
