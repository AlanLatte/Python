"""Here you can pass the postgres error codes with association python
exceptions."""

from psycopg2 import errorcodes
from app.pkg.models.exceptions import repository


__all__ = ["__aiopg__"]


__aiopg__ = {
    errorcodes.UNIQUE_VIOLATION: repository.UniqueViolation,
}
