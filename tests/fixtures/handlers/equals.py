"""Fixtures for the equals handler tests."""

import typing

import pytest


@pytest.fixture()
def check_array_equality() -> (
    typing.Callable[[typing.List[typing.Any], typing.List[typing.Any]], bool]
):
    def wrapped(actual: typing.List[typing.Any], expected: typing.List[typing.Any]):
        return all(a in expected for a in actual)

    return wrapped
