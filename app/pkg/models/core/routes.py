"""Model for contains ``APIRouter`` instance."""

from dataclasses import dataclass
from typing import Tuple

from fastapi import APIRouter, FastAPI

__all__ = ["Routes"]


@dataclass(frozen=True)
class Routes:
    """Frozen model for storage all ``APIRouter``.

    Attributes:
        routers:
            Tuple of ``APIRouter`` instances.
    """

    routers: Tuple[APIRouter, ...]

    def register_routes(self, app: FastAPI):
        """Include ``APIRouter`` to the ``FastAPI`` application instance.

        Notes:
            Function used ``FastAPI.include_router``.

        See Also:
            https://fastapi.tiangolo.com/advanced/routers/

        Args:
            app: ``FastAPI`` application instance.

        Examples:
            For register routes, you **must** provide routers to model.::

                >>> from app.internal.routes import auth, user
                >>> __routes__ = Routes(
                ...    routers=(
                ...        user.router,
                ...        auth.router
                ...    )
                ...)

            If you call :meth:`.register_routes`, all routes from *self.routers* will be
            included to the ``FastAPI`` instance.::

                >>> from fastapi import FastAPI

                >>> app = FastAPI()
                >>> __routes__.register_routes(app=app)

        Returns:
            None
        """

        for router in self.routers:
            app.include_router(router)
