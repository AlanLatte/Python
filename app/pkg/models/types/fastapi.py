from typing import TypeVar

from fastapi import FastAPI

FastAPIInstance = TypeVar("FastAPIInstance", bound=FastAPI)  # noqa: Types
