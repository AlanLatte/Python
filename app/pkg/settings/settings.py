"""
Module for load settings form `.env` or
    if server running with parameter `dev` from `.env.dev`
"""

from functools import lru_cache

import pydantic
from dotenv import find_dotenv
from pydantic.env_settings import BaseSettings

__all__ = ["Settings", "get_settings"]

from pydantic.types import PositiveInt, SecretStr


class _Settings(BaseSettings):
    class Config:
        """Configuration of settings."""

        #: str: env file encoding.  #Unresolved reference
        env_file_encoding = "utf-8"
        #: str: allow custom fields in model.  #Unresolved reference
        arbitrary_types_allowed = True


class Settings(_Settings):
    """Server settings. Formed from `.env` or `.env.dev`."""

    # Postgres
    POSTGRES_HOST: pydantic.AnyUrl
    POSTGRES_PORT: PositiveInt
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_DATABASE_NAME: str

    # Redis
    REDIS_HOST: pydantic.AnyUrl
    REDIS_PORT: PositiveInt
    REDIS_PASSWORD: SecretStr




@lru_cache()
def get_settings(env_file: str = ".env") -> Settings:
    """Create settings instance."""

    return Settings(_env_file=find_dotenv(env_file))
