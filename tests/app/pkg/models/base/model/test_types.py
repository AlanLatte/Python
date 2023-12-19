"""Test manual wrote types."""

from typing import List

import pydantic
import pytest

from app.pkg.models.base import BaseModel


async def test_native_types(create_model):
    class TestModel(BaseModel):
        some_value: int
        some_value_two: str

    model = await create_model(TestModel)
    assert isinstance(model.some_value, int)
    assert isinstance(model.some_value_two, str)


async def test_native_types_miss_type():
    class TestModel(BaseModel):
        some_value: int
        some_value_two: str

    with pytest.raises(pydantic.ValidationError):
        TestModel(some_value="STRING_TYPE", some_value_two=2)


async def test_convert_native_types():
    class TestModel(BaseModel):
        some_value: int
        some_value_two: str

    model = TestModel(some_value="1", some_value_two=2)
    assert isinstance(model.some_value, int)
    assert isinstance(model.some_value_two, str)
    assert model.some_value == 1
    assert model.some_value_two == "2"


async def test_native_types_with_default():
    class TestModel(BaseModel):
        some_value: int = 1
        some_value_two: str = "1"

    model = TestModel()
    assert isinstance(model.some_value, int)
    assert isinstance(model.some_value_two, str)
    assert model.some_value == 1
    assert model.some_value_two == "1"


async def test_native_types_with_default_and_value(create_model):
    class TestModel(BaseModel):
        some_value: int = 1
        some_value_two: str = "1"

    model = await create_model(TestModel, some_value=2, some_value_two="2")
    assert isinstance(model.some_value, int)
    assert isinstance(model.some_value_two, str)
    assert model.some_value == 2
    assert model.some_value_two == "2"


async def test_object():
    class TestModel(BaseModel):
        some_value: int
        some_value_two: str

    class AnotherTestModel(BaseModel):
        some_class: TestModel

    model = AnotherTestModel(some_class=TestModel(some_value=1, some_value_two="1"))
    assert isinstance(model.some_class, TestModel)
    assert isinstance(model.some_class.some_value, int)
    assert isinstance(model.some_class.some_value_two, str)
    assert model.some_class.some_value == 1
    assert model.some_class.some_value_two == "1"


async def test_object_with_default():
    class TestModel(BaseModel):
        some_value: int = 1
        some_value_two: str = "1"

    class AnotherTestModel(BaseModel):
        some_class: TestModel = TestModel()

    model = AnotherTestModel()
    assert isinstance(model.some_class, TestModel)
    assert isinstance(model.some_class.some_value, int)
    assert isinstance(model.some_class.some_value_two, str)
    assert model.some_class.some_value == 1
    assert model.some_class.some_value_two == "1"


async def test_object_with_default_and_value():
    class TestModel(BaseModel):
        some_value: int = 1
        some_value_two: str = "1"

    class AnotherTestModel(BaseModel):
        some_class: TestModel = TestModel()

    model = AnotherTestModel(some_class=TestModel(some_value=2, some_value_two="2"))
    assert isinstance(model.some_class, TestModel)
    assert isinstance(model.some_class.some_value, int)
    assert isinstance(model.some_class.some_value_two, str)
    assert model.some_class.some_value == 2
    assert model.some_class.some_value_two == "2"


async def test_list_of_native_types():
    class TestModel(BaseModel):
        some_value: int
        some_value_two: str

    class AnotherTestModel(BaseModel):
        some_list: List[TestModel]

    model = AnotherTestModel(some_list=[TestModel(some_value=1, some_value_two="1")])
    assert isinstance(model.some_list, list)
    assert model.some_list[0].some_value == 1
    assert model.some_list[0].some_value_two == "1"


async def test_list_of_native_types_with_default():
    class TestModel(BaseModel):
        some_value: int = 1
        some_value_two: str = "1"

    class AnotherTestModel(BaseModel):
        some_list: List[TestModel] = [TestModel()]

    model = AnotherTestModel()
    assert isinstance(model.some_list, list)
    assert model.some_list[0].some_value == 1
    assert model.some_list[0].some_value_two == "1"


async def test_list_of_native_types_with_default_and_value():
    class TestModel(BaseModel):
        some_value: int = 1
        some_value_two: str = "1"

    class AnotherTestModel(BaseModel):
        some_list: List[TestModel] = [TestModel()]

    model = AnotherTestModel(some_list=[TestModel(some_value=2, some_value_two="2")])
    assert isinstance(model.some_list, list)
    assert model.some_list[0].some_value == 2
    assert model.some_list[0].some_value_two == "2"
