"""Global point for collected routers."""

from app.pkg.models.core.routes import Routes
from app.internal.routes import auth, user

__all__ = ["__routes__"]


__routes__ = Routes(routers=(user.router, auth.router))
"""Global point for collected routers.

This snippet from app/internal/pkg/models/routes.py:

Examples:
    When you using routers with `FastAPI`::
        >>> from fastapi import FastAPI
        >>> app = FastAPI()
        >>> __routes__.register_routes(app=app)
"""
