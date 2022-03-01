from dataclasses import dataclass, field
from typing import Callable, List, Optional

from dependency_injector import containers
from fastapi import FastAPI

__all__ = ["Container", "Containers"]


@dataclass(frozen=True)
class Container:
    """Model for contain single container."""

    #: containers.Container: dependency_injector declarative container callable object.
    container: Callable[..., containers.Container]

    #: List[str]: Array of packages to which the injector will be available.
    #  Default: ["app"]
    packages: List[str] = field(default_factory=lambda: ["app"])


@dataclass(frozen=True)
class Containers:
    """Frozen dataclass model, for contains all declarative containers."""

    #: str: __name__ of main package.
    pkg_name: str

    #: List[Container]: List of `Container` model.
    containers: List[Container]

    def wire_packages(self, app: Optional[FastAPI] = None):
        """Wire packages to the declarative containers.

        Args:
            app: Optional ``FastAPI`` instance.
                if passed, the containers will be written to the application context.

        Returns:
            None
        """
        for container in self.containers:
            cont = container.container()
            cont.wire(packages=[self.pkg_name, *container.packages])
            if app:
                setattr(app, container.__name__, cont)
