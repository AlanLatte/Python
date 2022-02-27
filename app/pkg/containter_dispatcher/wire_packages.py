"""Wire packages to the declarative containers."""

from dependency_injector.containers import Container
from typing import Callable, List

__all__ = ["wire_packages"]


def wire_packages(
    container: Callable[..., Container],
    pkg_name: str,
    packages: List[str],
) -> None:
    """Wire packages to the declarative containers.

    Args:
        container: Declarative container of dependency-injector.
        pkg_name: __name__ of main package.
        packages: Array of packages to which the injector will be available.

    Returns:
        None
    """

    container().wire(packages=[pkg_name, *packages])
