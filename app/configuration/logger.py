"""WSGI Logger configuration."""

import logging

__all__ = ["EndpointFilter"]


class EndpointFilter(logging.Filter):
    """Filter for logging messages by endpoint.

    Attributes:
        endpoint:
            Name of endpoint to filter messages by.
    """

    endpoint: str

    def __init__(self, endpoint: str, *args, **kwargs):
        """Initialize filter.

        Args:
            endpoint:
                Name of endpoint to filter messages by.
        """

        self.endpoint = endpoint
        super().__init__(*args, **kwargs)

    def filter(self, record: logging.LogRecord) -> bool:
        """Filter for logging messages by endpoint.

        Args:
            record:
                Record of logging message.

        Returns:
            True if endpoint is not in message, False otherwise
        """

        return record.getMessage().find(self.endpoint) == -1
