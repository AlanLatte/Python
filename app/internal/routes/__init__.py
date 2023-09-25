"""Router layer."""

from app.internal.routes import auth, user
from app.pkg.models.core.routes import Routes

__all__ = ["__routes__"]


__routes__ = Routes(routers=(user.router, auth.router))
"""Global point for collected routers.

__routes__ is a :class:`.Routes` instance that contains all routers in your application.

Examples:
    After declaring all routers, you need to register them in your application::
    
        >>> from fastapi import FastAPI
        >>> app = FastAPI()
        >>> __routes__.register_routes(app=app)
"""
