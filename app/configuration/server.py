"""Server configuration."""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.configuration.events import on_startup, on_shutdown
from app.configuration.logger import EndpointFilter
from app.internal.pkg.middlewares.handle_http_exceptions import handle_api_exceptions
from app.internal.pkg.middlewares.metrics import metrics
from app.internal.pkg.middlewares.prometheus import PrometheusMiddleware
from app.internal.routes import __routes__
from app.pkg.models.base import BaseAPIException
from app.pkg.models.types.fastapi import FastAPITypes
from app.pkg.settings import settings

__all__ = ["Server"]


class Server:
    """Register all requirements for correct work of server instance."""

    __app: FastAPI
    __app_name: str = settings.API_INSTANCE_APP_NAME

    def __init__(self, app: FastAPI):
        self.__app = app
        self._register_routes(app)
        self._register_events(app)
        self._register_middlewares(app)
        self._register_http_exceptions(app)

    def get_app(self) -> FastAPI:
        """Get current application instance.

        Returns: ``FastAPI`` application instance.
        """
        return self.__app

    @staticmethod
    def _register_events(app: FastAPITypes.FastAPIInstance) -> None:
        """Register default events.

        Args:
            app: ``FastAPI`` application instance.

        Returns: None
        """

        app.on_event("startup")(on_startup)
        app.on_event("shutdown")(on_shutdown)

    @staticmethod
    def _register_routes(app: FastAPITypes.FastAPIInstance) -> None:
        """Include routers in ``FastAPI`` instance from ``__routes__``.

        Args:
            app: ``FastAPI`` application instance.

        Returns: None
        """

        __routes__.register_routes(app)

    @staticmethod
    def _register_http_exceptions(app: FastAPITypes.FastAPIInstance) -> None:
        """Register http exceptions.

        FastAPIInstance handle BaseApiExceptions raises inside functions.

        Args:
            app: ``FastAPI`` application instance

        Returns: None
        """

        app.add_exception_handler(BaseAPIException, handle_api_exceptions)

    @staticmethod
    def __register_cors_origins(app: FastAPITypes.FastAPIInstance) -> None:
        """Register cors origins. In production, you should use only trusted origins.

        Warnings:
            For default this method is not secure.
            You **should use it only for development.**
            Read more about CORS: https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS

        Args:
            app: ``FastAPI`` application instance.

        Returns: None
        """

        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def __register_prometheus(self, app: FastAPITypes.FastAPIInstance) -> None:
        """Register prometheus middleware.

        Args:
            app: ``FastAPI`` application instance.

        Returns: None
        """

        app.add_middleware(
            PrometheusMiddleware,
            open_telemetry_grpc_endpoint=settings.OPEN_TELEMETRY_GRPC_ENDPOINT,
            app_name=self.__app_name,
        )

        self.__register_metrics_collector(
            app=app,
            prometheus=PrometheusMiddleware(
                app=app,
                open_telemetry_grpc_endpoint=settings.OPEN_TELEMETRY_GRPC_ENDPOINT,
                app_name=self.__app_name,
            ),
        )

    def __register_metrics_collector(
        self,
        app: FastAPITypes.FastAPIInstance,
        prometheus: PrometheusMiddleware,
    ) -> None:
        """Expose internal aggregated metrics to public endpoint.

        Args:
            app: ``FastAPI`` application instance.

        Returns: None
        """

        metrics_endpoint = "/metrics"
        app.add_route(metrics_endpoint, metrics)
        prometheus.inject_tracer()
        self.__filter_logs(metrics_endpoint)

    def _register_middlewares(self, app) -> None:
        """Apply routes middlewares."""

        self.__register_cors_origins(app)
        self.__register_prometheus(app)

    @staticmethod
    def __filter_logs(endpoint: str) -> None:
        """Filter ignore /metrics in uvicorn logs."""

        logging.getLogger("uvicorn.access").addFilter(EndpointFilter(endpoint=endpoint))
