"""Middleware for expose internal metrics to public endpoint."""

from prometheus_client.openmetrics.exposition import (
    CONTENT_TYPE_LATEST,
    generate_latest,
)

from starlette.requests import Request
from starlette.responses import Response
from prometheus_client.registry import REGISTRY

__all__ = ["metrics"]


def metrics(request: Request) -> Response:
    _ = request

    return Response(
        generate_latest(REGISTRY), headers={"Content-Type": CONTENT_TYPE_LATEST}
    )
