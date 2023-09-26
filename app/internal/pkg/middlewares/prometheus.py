"""Prometheus middleware."""

import time
from typing import Tuple

from opentelemetry import trace
from prometheus_client import Counter, Gauge, Histogram
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Match
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from starlette.types import ASGIApp

from app.internal.pkg.middlewares.handle_http_exceptions import (
    handle_api_exceptions,
    handle_internal_exception,
)
from app.pkg.models.base import BaseAPIException
from app.pkg.models.types.fastapi import FastAPITypes

__all__ = ["PrometheusMiddleware"]


class PrometheusMiddleware(BaseHTTPMiddleware):
    """Middleware for collecting metrics from FastAPI application."""

    app: FastAPITypes.instance

    __filter_unhandled_paths: bool
    __app_name: str

    __INFO = Gauge("fastapi_app_info", "FastAPI application information.", ["app_name"])
    __REQUESTS = Counter(
        "fastapi_requests_total",
        "Total count of requests by method and path.",
        ["method", "path", "app_name"],
    )
    __RESPONSES = Counter(
        "fastapi_responses_total",
        "Total count of responses by method, path and status codes.",
        ["method", "path", "status_code", "app_name"],
    )
    __REQUESTS_PROCESSING_TIME = Histogram(
        "fastapi_requests_duration_seconds",
        "Histogram of requests processing time by path (in seconds)",
        ["method", "path", "app_name"],
    )
    __EXCEPTIONS = Counter(
        "fastapi_exceptions_total",
        "Total count of exceptions raised by path and exception type",
        ["method", "path", "exception_type", "app_name"],
    )
    __REQUESTS_IN_PROGRESS = Gauge(
        "fastapi_requests_in_progress",
        "Gauge of requests by method and path currently being processed",
        ["method", "path", "app_name"],
    )

    def __init__(
        self,
        app: ASGIApp,
        app_name: str = "api",
        filter_unhandled_paths: bool = True,
    ) -> None:
        super().__init__(app)
        self.__app_name = app_name
        self.__INFO.labels(app_name=self.__app_name).inc()
        self.__filter_unhandled_paths = filter_unhandled_paths

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        method = request.method
        path_template, is_handled_path = self.__get_path_template(request)

        if self.__is_path_filtered(is_handled_path):
            return await call_next(request)

        self.__REQUESTS_IN_PROGRESS.labels(
            method=method,
            path=path_template,
            app_name=self.__app_name,
        ).inc()
        self.__REQUESTS.labels(
            method=method,
            path=path_template,
            app_name=self.__app_name,
        ).inc()
        before_time = time.perf_counter()
        status_code = HTTP_500_INTERNAL_SERVER_ERROR
        try:
            response = await call_next(request)
        except (  # pylint: disable=broad-exception-caught
            BaseAPIException,
            Exception,
        ) as e:
            self.__EXCEPTIONS.labels(
                method=method,
                path=path_template,
                exception_type=type(e).__name__,
                app_name=self.__app_name,
            ).inc()
            if isinstance(e, BaseAPIException):
                return handle_api_exceptions(request=request, exc=e)
            return handle_internal_exception(request=request, exc=e)
        else:
            status_code = response.status_code
            after_time = time.perf_counter()
            span = trace.get_current_span()
            trace_id = trace.format_trace_id(span.get_span_context().trace_id)

            self.__REQUESTS_PROCESSING_TIME.labels(
                method=method,
                path=path_template,
                app_name=self.__app_name,
            ).observe(after_time - before_time, exemplar={"TraceID": trace_id})
        finally:
            self.__RESPONSES.labels(
                method=method,
                path=path_template,
                status_code=status_code,
                app_name=self.__app_name,
            ).inc()
            self.__REQUESTS_IN_PROGRESS.labels(
                method=method,
                path=path_template,
                app_name=self.__app_name,
            ).dec()

        return response

    @staticmethod
    def __get_path_template(request: Request) -> Tuple[str, bool]:
        for route in request.app.routes:
            match, _ = route.matches(request.scope)
            if match == Match.FULL:
                return route.path, True

        return request.url.path, False

    def __is_path_filtered(self, is_handled_path: bool) -> bool:
        return self.__filter_unhandled_paths and not is_handled_path
