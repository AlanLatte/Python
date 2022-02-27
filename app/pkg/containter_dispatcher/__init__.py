"""Register all declarative containers to the application instance."""

from typing import List
from .wire_packages import wire_packages


def register_container(pkg_name: str, packages: List[str] = None) -> None:
    """Function for register all containers.

    Args:
        pkg_name: __name__ of main package.
        packages: Optional array of packages to which the injector will be available.
            Default: `app.internal`
    Returns:
        None
    """

    if packages is None:
        packages = ["app.internal"]
    ...

