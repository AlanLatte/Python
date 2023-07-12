import operator
from dataclasses import dataclass, field
from typing import Callable, List, Optional, Type

from dependency_injector import containers, providers
from dependency_injector.containers import Container as _Container
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

    def wire_packages(
        self,
        app: Optional[FastAPI] = None,
        pkg_name: Optional[str] = None,
        unwire: bool = False,
    ):
        """Wire packages to the declarative containers.

        Args:
            app: Optional ``FastAPI`` instance.
                if passed, the containers will be written to the application context.
            pkg_name: Optional __name__ of running module.

            unwire: Optional bool parameter. If `True`, un wiring all containers.

        Returns:
            None
        """
        pkg_name = pkg_name if pkg_name else self.pkg_name
        for container in self.containers:
            cont = container.container()
            if unwire:
                cont.unwire()
                continue

            cont.wire(packages=[pkg_name, *container.packages])
            if app:
                setattr(app, container.container.__name__.lower(), cont)

    def set_environment(
        self,
        connector_class: Type[_Container],
        *,
        pkg_name: Optional[str] = None,
        testing: bool = False,
        database_configuration_path: str = "POSTGRES.DATABASE_NAME",
        prefix: Optional[str] = "test_",
    ) -> None:
        """Set environment for injection.

        Using `container.configuration` for rewrite
        `{{database_configuration_name}}` parameter in `settings`.

        Args:
            database_configuration_path: Pydantic settings field name that contains
                database name
            connector_class: Type of database connector
            testing: If `true` then adding prefix from argument `prefix`
                to database name
            pkg_name: Optional __name__ of running module.
            prefix: A `prefix` that can be concatenated with the database name

        Warnings:
            At v.2.6 it is not possible to set the value of a many-nested attribute.
            This realization only works for the first level of nesting.
            For this example it does not work:
                `POSTGRES.SOME.SOME.DATABASE_NAME`

        Returns:
            None
        """
        self.wire_packages(pkg_name=pkg_name, unwire=True)

        if testing:
            for container in self.containers:
                if not container.container.__name__ == connector_class.__name__:
                    continue

                conf: providers.Configuration = container.container().configuration
                pydantic_settings = conf.get_pydantic_settings()[0]
                database_name = operator.attrgetter(database_configuration_path)(
                    pydantic_settings,
                )

                # TODO: Make this better.
                #       Now it is not possible to set the value of a nested attribute.
                #       For example: `POSTGRES.SOME.SOME.DATABASE_NAME`
                #       This realization only works for the first level of nesting.
                setattr(
                    getattr(
                        pydantic_settings,
                        *database_configuration_path.split(".")[:-1],
                    ),
                    database_configuration_path.split(".")[-1],
                    f"{prefix}{database_name}",
                )

                conf.from_pydantic(pydantic_settings)

        self.wire_packages(pkg_name=pkg_name)

    @staticmethod
    def __setattr_nested(base, path, value):
        """Accept a dotted path to a nested attribute to set."""

        path, _, target = path.rpartition(".")
        for attribute_name in path.split("."):
            base = getattr(base, attribute_name)
        setattr(base, target, value)
