"""Main factory builder of ``FastAPI`` server."""

from fastapi import FastAPI

from app.configuration import __containers__
from app.configuration.server import Server


def create_app() -> FastAPI:
    """Create ``FastAPI`` application.

    `create_app` is a global point of your application.
    In `create_app` you can add all your middlewares, routes, dependencies, etc.
    required for global server startup.

    Examples:
        For start building your application, you should provide to uvicorn this point of
        your application::

            $ uvicorn app:create_app --reload

        When you need to connect TOKEN-based auth strategy, you can add dependency to
        ``FastAPI`` instance::

            >>> from fastapi import FastAPI, Depends
            >>> from app.internal.pkg.middlewares.x_auth_token import get_x_token_key
            >>> app = FastAPI(dependencies=[Depends(get_x_token_key)])
    """
    app = FastAPI()
    __containers__.wire_packages(app=app)
    return Server(app).get_app()
