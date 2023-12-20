"""Types for FastAPI application."""

from typing import TypeVar

from fastapi import FastAPI

__all__ = ["FastAPITypes"]


class FastAPITypes:
    instance = TypeVar("instance", bound=FastAPI)
