"""WSGI Logger configuration."""

import logging

__all__ = ["EndpointFilter"]


class EndpointFilter(logging.Filter):
    """Filter for logging messages by endpoint.

    Attributes:
        endpoint: endpoint name
    """

    endpoint: str

    def __init__(self, endpoint: str, *args, **kwargs):
        self.endpoint = endpoint
        super().__init__(*args, **kwargs)

    def filter(self, record: logging.LogRecord) -> bool:
        """Filter for logging messages by endpoint.

        Args:
            record: logging record

        Returns:
            True if endpoint is not in message, False otherwise
        """

        return record.getMessage().find(self.endpoint) == -1
