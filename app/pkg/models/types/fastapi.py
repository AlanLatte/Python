from typing import TypeVar

from fastapi import FastAPI

__all__ = ["FastAPITypes"]


class FastAPITypes:
    FastAPIInstance = TypeVar("FastAPIInstance", bound=FastAPI)  # noqa: Types
