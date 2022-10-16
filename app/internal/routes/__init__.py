"""Global point for collected routers."""

from app.internal.pkg.models import Routes
from app.internal.routes import auth, user

__all__ = ["__routes__"]


__routes__ = Routes(routers=(user.router, auth.router))
# TODO: Добавить документацию.
