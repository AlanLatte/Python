"""Tests for :meth:`.BaseModel.migrate()`."""
import decimal

import pydantic
import pytest

from app.pkg.models.base import BaseModel


async def test_with_some_missing_fields():
    class TestModel(BaseModel):
        some_value: int
        some_value_two: str

    class AnotherTestModel(BaseModel):
        some_value: int
        some_value_two: str
        some_value_three: str
        some_value_four: float

    model = TestModel(some_value=1, some_value_two="1")

    with pytest.raises(pydantic.ValidationError):
        model.migrate(AnotherTestModel)


async def test_model():
    class TestModel(BaseModel):
        some_value: int
        some_value_two: str
        some_value_three: str
        some_value_four: float

    class AnotherTestModel(BaseModel):
        some_value: int
        some_value_two: str

    model = TestModel(
        some_value=1,
        some_value_two="1",
        some_value_three="1",
        some_value_four=1.0,
    )
    another_model = model.migrate(AnotherTestModel)

    assert another_model.some_value == 1
    assert another_model.some_value_two == "1"


async def test_with_matching_keys():
    class TestModel(BaseModel):
        some_value: int
        some_value_two: str

    class AnotherTestModel(BaseModel):
        first: int
        second: str

    model = TestModel(some_value=1, some_value_two="1")
    another_model = model.migrate(
        AnotherTestModel,
        match_keys={"first": "some_value", "second": "some_value_two"},
    )

    assert another_model.first == 1
    assert another_model.second == "1"


@pytest.mark.repeat(5)
async def test_with_filling_mismatching_fields():
    class TestModel(BaseModel):
        some_value: int
        some_value_two: str

    class AnotherTestModel(BaseModel):
        some_value: int
        some_value_two: str
        some_value_three: str
        some_value_four: float

    model = TestModel(some_value=1, some_value_two="1")
    another_model = model.migrate(AnotherTestModel, random_fill=True)

    assert another_model.some_value == 1
    assert another_model.some_value_two == "1"
    assert another_model.some_value_three is not None
    assert another_model.some_value_four is not None


@pytest.mark.repeat(5)
async def test_with_extra_field():
    class TestModel(BaseModel):
        some_value: int
        some_value_two: str

    class AnotherTestModel(BaseModel):
        some_value: int
        some_value_two: str
        some_value_three: str
        some_value_four: decimal.Decimal

    model = TestModel(some_value=1, some_value_two="1")

    another_model = model.migrate(
        AnotherTestModel,
        extra_fields={
            "some_value_three": "1",
            "some_value_four": decimal.Decimal("1.0"),
        },
    )

    assert another_model.some_value == 1
    assert another_model.some_value_two == "1"
    assert another_model.some_value_three == "1"
    assert another_model.some_value_four == decimal.Decimal("1.0")
