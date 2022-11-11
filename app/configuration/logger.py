import logging

__all__ = ["EndpointFilter"]


class EndpointFilter(logging.Filter):
    endpoint: str

    def __init__(self, endpoint: str, *args, **kwargs):
        self.endpoint = endpoint
        super().__init__(*args, **kwargs)

    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find(self.endpoint) == -1
