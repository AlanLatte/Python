"""Global point to cached settings."""

from .settings import get_settings

__all__ = ["settings"]

settings = get_settings()
