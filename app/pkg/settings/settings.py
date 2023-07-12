"""Module for load settings form `.env` or if server running with parameter
`dev` from `.env.dev`"""
import pathlib
from functools import lru_cache

import pydantic
from dotenv import find_dotenv
from pydantic import validator
from pydantic.env_settings import BaseSettings
from pydantic.types import PositiveInt, SecretStr

from app.pkg.models import UserRole
from app.pkg.models.types import EncryptedSecretBytes

__all__ = ["Settings", "get_settings"]


class _Settings(BaseSettings):
    """Base settings. for all settings.

    Use double underscore for nested env variables.
    For example:
    - .env:

        TELEGRAM__TOKEN=...
        TELEGRAM__WEBHOOK_DOMAIN_URL=...

        LOGGER__PATH_TO_LOG="./src/logs"
        LOGGER__LEVEL="DEBUG"

        API_SERVER__HOST="127.0.0.1"
        API_SERVER__PORT=9191

    Warnings:
        In the case where a value is specified for the same Settings field in multiple
        ways, the selected value is determined as follows
        (in descending order of priority):

        1. Arguments passed to the Settings class initializer.
        2. Environment variables, e.g. my_prefix_special_function as described above.
        3. Variables loaded from a dotenv (.env) file.
        4. Variables loaded from the secrets directory.
        5. The default field values for the Settings model.

    See Also: https://docs.pydantic.dev/latest/usage/pydantic_settings/
    """

    class Config:
        """Configuration of settings."""

        #: str: env file encoding.
        env_file_encoding = "utf-8"
        #: str: allow custom fields in model.
        arbitrary_types_allowed = True
        #: bool: case-sensitive for env variables.
        case_sensitive = True
        #: str: delimiter for nested env variables.
        env_nested_delimiter = "__"


class Postgresql(_Settings):
    """Postgresql settings."""

    #: str: Postgresql host.
    HOST: str = "localhost"
    #: PositiveInt: positive int (x > 0) port of postgresql.
    PORT: PositiveInt = 5432
    #: str: Postgresql user.
    USER: str = "postgres"
    #: SecretStr: Postgresql password.
    PASSWORD: SecretStr = "postgres"
    #: str: Postgresql database name.
    DATABASE_NAME: str = "postgres"


class DefaultUser(_Settings):
    """Default user settings."""

    #: str: Default username.
    USERNAME: str = "admin"
    #: EncryptedSecretBytes: Default user password.
    PASSWORD: EncryptedSecretBytes = "admin_admin"
    #: UserRole: Enum validation of user role.
    ROLE: UserRole = UserRole.USER


class Redis(_Settings):
    """Redis settings."""

    #: str: Redis host.
    HOST: str = "localhost"
    #: PositiveInt: positive int (x > 0) port of redis.
    PORT: PositiveInt = 6379
    #: SecretStr: Redis password.
    PASSWORD: SecretStr = "redis_redis"


class JWT(_Settings):
    """JWT settings."""

    #: SecretStr: Key for encrypt payload in jwt.
    SECRET_KEY: SecretStr = "secret"
    #: str: Access token name in headers/body/cookies.
    ACCESS_TOKEN_NAME: str = "access_token"
    #: str: Refresh token name in headers/body/cookies.
    REFRESH_TOKEN_NAME: str = "refresh_token"


class Logging(_Settings):
    """Logging settings."""

    #: StrictStr: Level of logging which outs in std
    LEVEL: pydantic.StrictStr = "DEBUG"
    #: pathlib.Path: Path of saving logs on local storage.
    FILE_PATH: pathlib.Path = pathlib.Path("./src/logs")

    @validator("FILE_PATH")
    def __create_dir_if_not_exist(cls, v: pathlib.Path):
        """Create directory if not exist."""

        if not v.exists():
            v.mkdir(exist_ok=True, parents=True)
        return v


class APIServer(_Settings):
    """API settings."""
    # --- API SETTINGS ---
    #: str: Name of API service
    INSTANCE_APP_NAME: str = "API"
    #: str: API host.
    HOST: str = "localhost"
    #: PositiveInt: positive int (x > 0) port of API.
    PORT: PositiveInt = 8000

    # --- SECURITY SETTINGS ---
    #: SecretStr: X-ACCESS-TOKEN for access to API.
    X_ACCESS_TOKEN: SecretStr = "secret"
    #: JWT: JWT settings.
    JWT: JWT

    # --- OTHER SETTINGS ---
    #: Logging: Logging settings.
    LOGGER: Logging
    #: DefaultUser: Default user settings.
    DEFAULT_USER: DefaultUser

    # --- OPEN TELEMETRY SETTINGS ---
    #: str: Open Telemetry endpoint
    OPEN_TELEMETRY_GRPC_ENDPOINT: str


class Centrifugo(_Settings):
    #: str: Centrifugo host.
    HOST: str = "localhost"
    #: PositiveInt: positive int (x > 0) port of centrifugo.
    PORT: PositiveInt = 8001

class RabbitMQ(_Settings):
    """RabbitMQ settings."""

    #: str: RabbitMQ host.
    HOST: str = "localhost"
    #: PositiveInt: positive int (x > 0) port of rabbitmq.
    PORT: PositiveInt = 5672
    #: str: RabbitMQ user.
    USER: str = "rabbitmq"
    #: SecretStr: RabbitMQ password.
    PASSWORD: SecretStr = "rabbitmq"

class Settings(_Settings):
    """Server settings.

    Formed from `.env` or `.env.dev` if server running with parameter `dev`.
    """

    #: APIServer: API settings. Contains all settings for API.
    API: APIServer

    #: Postgresql: Postgresql settings.
    POSTGRES: Postgresql

    #: Redis: Redis settings.
    REDIS: Redis

    #: Centrifugo: Centrifugo settings.
    CENTRIFUGO: Centrifugo

    #: RabbitMQ: RabbitMQ settings.
    RABBITMQ: RabbitMQ

@lru_cache()
def get_settings(env_file: str = ".env") -> Settings:
    """Create settings instance."""

    return Settings(_env_file=find_dotenv(env_file))
