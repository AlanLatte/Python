"""Server configuration.

Collect or build all requirements for startup. Provide global point to
``Server`` instance.
"""

from app.internal.services import Services
from app.pkg.connectors import Connectors, PostgresSQL
from app.pkg.jwt import JWT
from app.pkg.models.core import Container, Containers
from app.pkg.models.core.containers import Resource

__all__ = ["__containers__"]


__containers__ = Containers(
    pkg_name=__name__,
    containers=[
        Container(container=Services),
        Container(container=JWT),
        Resource(
            container=Connectors,
            depends_on=[Container(container=PostgresSQL)],
        ),
    ],
)
"""
Containers: Containers needs for register all containers.
For start building you *MUST* call wire_packages.

Examples:
    When you using containers without `FastAPI`::
        >>> __containers__.wire_packages()

    When you using ``FastAPI`` server, you *MUST* pass an argument
    application instance::
        >>> from fastapi import FastAPI
        >>> app = FastAPI()
        >>> __containers__.wire_packages(app=app)
"""
