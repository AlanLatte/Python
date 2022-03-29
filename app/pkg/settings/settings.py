"""
Module for load settings form `.env` or
if server running with parameter `dev` from `.env.dev`
"""

from functools import lru_cache

from dotenv import find_dotenv
from pydantic.env_settings import BaseSettings
from pydantic.types import PositiveInt, SecretStr

__all__ = ["Settings", "get_settings"]


class _Settings(BaseSettings):
    class Config:
        """Configuration of settings."""

        #: str: env file encoding.
        env_file_encoding = "utf-8"
        #: str: allow custom fields in model.
        arbitrary_types_allowed = True


class Settings(_Settings):
    """Server settings. Formed from `.env` or `.env.dev`."""

    POSTGRES_HOST: str
    POSTGRES_PORT: PositiveInt
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_DATABASE_NAME: str

    REDIS_HOST: str
    REDIS_PORT: PositiveInt
    REDIS_PASSWORD: SecretStr

    RABBITMQ_HOST: str
    RABBITMQ_PORT: PositiveInt
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: SecretStr


@lru_cache()
def get_settings(env_file: str = ".env") -> Settings:
    """Create settings instance."""
    print("=====================")
    print(find_dotenv(".env"))
    print("=====================")
    return Settings(_env_file=find_dotenv(env_file))
