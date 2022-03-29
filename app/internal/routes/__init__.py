"""Global point for collected routers."""

from app.internal.pkg.models import Routes
from app.internal.routes import user

__all__ = ["__routes__"]


__routes__ = Routes(routers=(user.router,))
# TODO: Добавить документацию.
