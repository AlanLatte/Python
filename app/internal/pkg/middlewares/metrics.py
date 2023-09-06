"""Middleware for expose internal metrics to public endpoint."""

from prometheus_client.openmetrics.exposition import (
    CONTENT_TYPE_LATEST,
    generate_latest,
)
from prometheus_client.registry import REGISTRY
from starlette.requests import Request
from starlette.responses import Response

__all__ = ["metrics"]


def metrics(request: Request) -> Response:
    """Expose internal metrics to public endpoint."""

    _ = request

    return Response(
        generate_latest(REGISTRY),
        headers={"Content-Type": CONTENT_TYPE_LATEST},
    )
