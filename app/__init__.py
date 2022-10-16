"""Main factory builder of ``FastAPI`` server."""

from fastapi import FastAPI
from app.configuration import __containers__
from app.configuration.server import Server


def create_app() -> FastAPI:
    app = FastAPI()
    __containers__.wire_packages(app=app)
    return Server(app).get_app()
