from dataclasses import dataclass, field
from typing import Callable, List, Optional, Type, Union

from dependency_injector import containers, providers
from dependency_injector.containers import Container, Container as _Container
from fastapi import FastAPI

from app.pkg import handlers

__all__ = ["Container", "Containers", "Resource"]


@dataclass(frozen=True)
class Resource:
    #: containers.Container: dependency_injector resource container callable object.
    container: Type[Container]

    #: List[Callable[..., containers.Container]]: List of dependency_injector containers.
    #  This containers MUST be wired to the main container.
    #  Default: []
    depends_on: List[containers.Container] = field(default_factory=list)

    #: List[str]: Array of packages to which the injector will be available.
    #  Default: ["app"]
    packages: List[str] = field(default_factory=lambda: ["app"])


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
    containers: List[Union[Container, Resource]]

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

        Notes:
            If you want to use the injector in other modules, you need to set
            ``pkg_name`` parameter to the name of the module in which the injector
            is running.
            For example, you have module tree like:
            ```
            ProjectName
            ├── app
            │    ├── api
            │    │   ├── endpoints
            │    │   │   └── users.py
            │    │   └── __init__.py
            │    ├── internal
            │    │   ├── repository
            │    │   │   └── postgresql
            │    │   └── __init__.py
            │    ├── pkg
            │    │   ├── connectors
            │    │   │   └── postgresql
            │    │   └── __init__.py
            │
            └── tests
                ├── api
                │   ├── endpoints
                │   │   └── users.py
                ...
            ```

            If you want to use the injector in ``users.py`` endpoints, you need to
            set ``pkg_name="app.api.endpoints"`` in ``wire_packages`` method.

            But you also can set ``pkg_name="app"`` for use injector in all modules
                in the project (expect tests).
            And you can set ``pkg_name="tests"`` for use injector in all modules
            in the project (with tests).


        Returns:
            None
        """
        pkg_name = pkg_name if pkg_name else self.pkg_name
        for container in self.containers:
            self.__wire(container, unwire, pkg_name, app)

            if not isinstance(container, Resource):
                continue

            for dep in container.depends_on:
                self.__wire(dep, unwire, pkg_name, app)

    @staticmethod
    def __wire(
        container: Union[Container, Resource],
        unwire: bool,
        pkg_name: str,
        app: Optional[FastAPI] = None,
    ) -> Container:
        """Wire container to the declarative containers.

        Args:
            container: Container or Resource model.
            unwire: Optional bool parameter. If `True`, un wiring all containers.
            pkg_name: Optional __name__ of running module.
            app: Optional ``FastAPI`` instance.
                if passed, the containers will be written to the application context.

        Returns:
            ``Container``
        """

        cont = container.container()

        if unwire:
            cont.unwire()
            return cont

        cont.wire(packages=[pkg_name, *container.packages])

        if app:
            setattr(app, container.container.__name__.lower(), cont)

        return cont

    def set_environment(
        self,
        connectors: List[Type[_Container]],
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
            connectors: Type of database connector
            testing: If `true` then adding prefix from argument `prefix`
                to database name
            pkg_name: Optional __name__ of running module.
            prefix: A `prefix` that can be concatenated with the database name

        Returns:
            None
        """
        self.wire_packages(pkg_name=pkg_name, unwire=True)

        if testing:
            for container in self.containers:
                if not (
                    container.container.__name__
                    in [_class.__name__ for _class in connectors]
                    or type(container) is Resource
                ):
                    continue

                for _container in container.depends_on:
                    self.__patch_container_configuration(
                        _container, database_configuration_path, prefix
                    )

        self.wire_packages(pkg_name=pkg_name)

    @staticmethod
    def __patch_container_configuration(
        container: Container, database_configuration_path: str, prefix: str
    ) -> Optional[_Container]:
        """Patch container configuration.

        Args:
            container: ``Container`` for patch configuration
            database_configuration_path: Pydantic settings field name that contains
                database name
            prefix: A `prefix` that can be concatenated with the database name

        Returns:
            ``Container`` with patched configuration
        """

        conf: providers.Configuration = container.container().configuration

        pydantic_settings = conf.get_pydantic_settings()[0]

        database_name = handlers.rec_getattr(
            pydantic_settings, database_configuration_path
        )

        handlers.rec_setattr(
            pydantic_settings, database_configuration_path, prefix + database_name
        )

        pydantic_settings.POSTGRES.DSN = pydantic_settings.POSTGRES.DSN.replace(
            database_name, prefix + database_name
        )

        conf.from_pydantic(pydantic_settings)

        return container
