from functools import wraps
from typing import List, Type, Union

import pydantic
from psycopg2.extras import RealDictRow  # type: ignore

from app.pkg.models.base import Model
from app.pkg.models.exceptions.repository import EmptyResult

from .handle_exception import handle_exception

__all__ = ["collect_response"]


def collect_response(fn):
    """

    Args:
        fn: Target function that contains a query in postgresql.

    Returns:
        The model that is specified in type hints of `fn`.

    Raises:
        EmptyResult: when query of `fn` returns None.

    """

    @wraps(fn)
    @handle_exception
    async def inner(
        *args: object,
        **kwargs: object,
    ) -> Union[List[Type[Model]], Type[Model]]:
        response = await fn(*args, **kwargs)
        if not response:
            raise EmptyResult
        return pydantic.parse_obj_as(
            (ann := fn.__annotations__["return"]),
            await __convert_response(response=response, annotations=str(ann)),
        )

    return inner


async def __convert_response(response: RealDictRow, annotations: str):
    """
    Converts the response of the request to an List of models or to a single model.
    Args:
        response: Response of aiopg query.
        annotations: Annotations of `fn`.

    Returns: List[`Model`] if List is specified in the type annotations,
            or a single `Model` if `Model` is specified in the type annotations.
    """
    r = response.copy()
    if annotations.replace("typing.", "").startswith("List"):
        return [await __convert_memory_viewer(item) for item in r]
    return await __convert_memory_viewer(r)


async def __convert_memory_viewer(r: RealDictRow):
    """Convert memory viewer in bytes.

    Notes: aiopg returns memory viewer in query response,
        when in database type of cell `bytes`.
    """
    for key, value in r.items():
        if isinstance(value, memoryview):
            r[key] = value.tobytes()
    return r
