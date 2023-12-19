"""Here you can pass the postgres error codes with association python
exceptions."""

from psycopg2 import errorcodes

from app.pkg.models.exceptions import (
    city,
    contacts,
    country,
    direction,
    repository,
    skill,
    partners,
    skill_levels,
)

__all__ = ["__aiopg__", "__constrains__"]


__aiopg__ = {
    errorcodes.UNIQUE_VIOLATION: repository.UniqueViolation,
}

# TODO: Make this dict more flexible.
#       Like `Container` class in `/app/pkg/models/core/container.py`
__constrains__ = {
    **city.__constrains__,
    **country.__constrains__,
    **direction.__constrains__,
    **skill.__constrains__,
    **skill_levels.__constrains__,
    **contacts.__constrains__,
    **partners.__constrains__,
}
