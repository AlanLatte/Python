"""Main factory builder of ``FastAPI`` server.
from app.internal.pkg.middlewares.x_auth_token import get_x_token_key

    app = FastAPI(dependencies=[Depends(get_x_token_key)])
    if you need x-auth-token auth
"""

from fastapi import FastAPI
from app.configuration import __containers__
from app.pkg.models.types.server import Server


def create_app() -> FastAPI:
    app = FastAPI()
    __containers__.wire_packages(app=app)
    return Server(app).get_app()
