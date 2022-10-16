"""
Module for load settings form `.env` or
if server running with parameter `dev` from `.env.dev`
"""
import pathlib
from functools import lru_cache

import pydantic
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

    # JWT
    JWT_SECRET_KEY: SecretStr
    JWT_ACCESS_TOKEN_NAME: str
    JWT_REFRESH_TOKEN_NAME: str

    RABBITMQ_HOST: str
    RABBITMQ_PORT: PositiveInt
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: SecretStr

    OTP_KEY: SecretStr

    # logger
    LOGGER_LEVEL: pydantic.StrictStr
    LOGGER_FILE_PATH: pathlib.Path

    @pydantic.validator("LOGGER_FILE_PATH")
    def check_secrets_dir_exists(cls, v: pathlib.Path) -> pathlib.Path:
        if not v.parent.exists():
            v.parent.mkdir(parents=True, exist_ok=True)
        return v


@lru_cache()
def get_settings(env_file: str = ".env") -> Settings:
    """Create settings instance."""
    print("=====================")
    print(find_dotenv(".env"))
    print("=====================")
    return Settings(_env_file=find_dotenv(env_file))
