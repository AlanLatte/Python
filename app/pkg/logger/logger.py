"""Methods for working with logger."""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from app.pkg.settings import settings

_log_format = (
    "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%("
    "funcName)s(%(lineno)d) - %(message)s "
)


def get_file_handler(file_name: str) -> RotatingFileHandler:
    """Get file handler for logger.

    Args:
        file_name:
            Name of the file to write logs.

    Notes:
        The file will be created in the directory
        specified in the :attr:`.Settings.API.LOGGER.FOLDER_PATH` parameter.

        If the directory does not exist, it will be created.

        When the file size exceeds 5 MB, the file will be rotated.

    Warnings:
        If the server disk is full,
        the file will not be rotated and the API service
        will stop working.

    Returns:
        File handler for logger.
    """

    Path(file_name).absolute().parent.mkdir(exist_ok=True, parents=True)
    file_handler = RotatingFileHandler(
        filename=file_name,
        maxBytes=5242880,
        backupCount=10,
    )
    file_handler.setFormatter(logging.Formatter(_log_format))
    return file_handler


def get_stream_handler():
    """Get stream handler for logger."""

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter(_log_format))
    return stream_handler


def get_logger(name):
    """Get logger.

    Args:
        name:
            Name of the logger.

    Returns:
        LoggerLevel instance.

    Examples:
        ::

            >>> from app.pkg.logger import get_logger
            >>> logger = get_logger(__name__)
            >>> logger.info("Hello, World!")
            2021-01-01 00:00:00,000 - [INFO] - app.pkg.logger - (logger.py).get_logger(43) - Hello, World!  # pylint: disable=line-too-long
    """
    logger = logging.getLogger(name)
    file_path = str(
        Path(
            settings.API.LOGGER.FOLDER_PATH,
            f"{settings.API.INSTANCE_APP_NAME}.log",
        ).absolute(),
    )
    logger.addHandler(get_file_handler(file_name=file_path))
    logger.addHandler(get_stream_handler())
    logger.setLevel(settings.API.LOGGER.LEVEL.upper())
    return logger
