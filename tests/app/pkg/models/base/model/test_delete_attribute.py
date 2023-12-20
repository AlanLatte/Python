"""Testing the :meth:`BaseModel.delete_attribute()`."""

import pytest

from app.pkg.models.base import BaseModel


async def test_delete_attribute():
    class TestModel(BaseModel):
        some_value: int = 1
        some_value_two: str = "1"

    model = TestModel(some_value=2, some_value_two="2")
    assert model.some_value == 2
    assert model.some_value_two == "2"

    with pytest.raises(AttributeError):
        model.delete_attribute("some_value")
        _ = model.some_value

    assert model.some_value_two == "2"


async def test_delete_attribute_with_default():
    class TestModel(BaseModel):
        some_value: int = 1
        some_value_two: str = "1"

    model = TestModel()
    assert model.some_value == 1
    assert model.some_value_two == "1"

    with pytest.raises(AttributeError):
        model.delete_attribute("some_value")
        _ = model.some_value

    assert model.some_value_two == "1"
