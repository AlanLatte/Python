"""Tests for :meth:`.BaseModel.to_dict()`."""

import datetime
import decimal
import typing
import uuid

import pydantic
import pytest
from pydantic import UUID4

from app.pkg.models.base import BaseModel


async def test_cast_types_base():
    class TestModel(BaseModel):
        some_value: int
        some_value_two: str
        some_value_three: decimal.Decimal
        some_value_four: bool

    model = TestModel(
        some_value="1",
        some_value_two=2,
        some_value_three=0.0,
        some_value_four="False",
    )
    dict_model = model.to_dict()

    assert isinstance(dict_model["some_value"], int)
    assert isinstance(dict_model["some_value_two"], str)
    assert isinstance(dict_model["some_value_three"], decimal.Decimal)
    assert isinstance(dict_model["some_value_four"], bool)

    assert dict_model["some_value"] == 1
    assert dict_model["some_value_two"] == "2"
    assert dict_model["some_value_three"] == decimal.Decimal("0.0")


async def test_cast_types_base_with_default():
    class TestModel(BaseModel):
        some_value: int = 1
        some_value_two: str = "1"
        some_value_three: typing.List[str] = ["1", "2", "3"]
        some_value_four: bool = False

    model = TestModel()
    dict_model = model.to_dict()

    assert dict_model["some_value"] == 1
    assert dict_model["some_value_two"] == "1"
    assert dict_model["some_value_three"] == ["1", "2", "3"]
    assert isinstance(dict_model["some_value_four"], bool)


async def test_complex_types_dict():
    class TestModel(BaseModel):
        some_value: dict

    model = TestModel(some_value={"key": "value"})
    dict_model = model.to_dict()

    assert isinstance(dict_model["some_value"], dict)
    assert dict_model["some_value"] == {"key": "value"}


async def test_complex_types_list():
    class TestModel(BaseModel):
        some_value: list

    model = TestModel(some_value=["key", "value"])
    dict_model = model.to_dict()

    assert isinstance(dict_model["some_value"], list)
    assert dict_model["some_value"] == ["key", "value"]


async def test_cast_to_string_complex_types_tuple():
    class TestModel(BaseModel):
        some_value: tuple

    model = TestModel(some_value=("key", "value"))
    dict_model = model.to_dict()

    assert isinstance(dict_model["some_value"], list)
    assert dict_model["some_value"] == ["key", "value"]


async def test_cast_to_string_complex_types_set():
    class TestModel(BaseModel):
        some_value: UUID4

    model = TestModel(some_value=uuid.uuid4())
    dict_model = model.to_dict()

    assert isinstance(dict_model["some_value"], str)


async def test_cast_to_string_complex_types_secret_without_deciphering():
    class TestModel(BaseModel):
        some_value: pydantic.SecretStr
        some_value_two: pydantic.SecretBytes

    model = TestModel(some_value="key", some_value_two="value")
    dict_model = model.to_dict()
    assert isinstance(dict_model["some_value"], str)
    assert isinstance(dict_model["some_value_two"], str)


async def test_cast_to_string_complex_types_secret_with_deciphering():
    class TestModel(BaseModel):
        some_value: pydantic.SecretStr
        some_value_two: pydantic.SecretBytes

    model = TestModel(some_value="key", some_value_two="value")
    dict_model = model.to_dict(show_secrets=True)

    assert isinstance(dict_model["some_value"], str)
    assert isinstance(dict_model["some_value_two"], str)

    assert dict_model["some_value"] == "key"
    assert dict_model["some_value_two"] == "value"


async def test_cast_to_string_complex_types_list_with_deciphering(create_model):
    class TestModel(BaseModel):
        some_value: pydantic.SecretStr
        some_value_two: typing.List[pydantic.SecretBytes]

    model = await create_model(TestModel)
    dict_model = model.to_dict(show_secrets=True)

    assert isinstance(dict_model["some_value"], str)
    assert isinstance(dict_model["some_value_two"], list)
    for item in dict_model["some_value_two"]:
        assert isinstance(item, str)


async def test_cast_to_string_complex_types_dict_with_deciphering(create_model):
    class TestModel(BaseModel):
        some_value: pydantic.SecretStr
        some_value_two: typing.Dict[str, typing.List[pydantic.SecretStr]]

    model = await create_model(TestModel)
    dict_model = model.to_dict(show_secrets=True)

    assert isinstance(dict_model["some_value"], str)
    assert isinstance(dict_model["some_value_two"], dict)
    for item in dict_model["some_value_two"].values():
        assert isinstance(item, list)
        for item_2 in item:
            assert isinstance(item_2, str)


async def test_cast_to_string_complex_types_tuple_with_deciphering(create_model):
    class TestModel(BaseModel):
        some_value: pydantic.SecretStr
        some_value_two: typing.Tuple[
            typing.Dict[str, typing.List[typing.Dict[str, pydantic.SecretStr]]],
        ]

    model = await create_model(TestModel)
    dict_model = model.to_dict(show_secrets=True)
    assert isinstance(dict_model["some_value"], str)
    assert isinstance(dict_model["some_value_two"], list)
    assert isinstance(dict_model["some_value_two"][0], dict)

    for key, value in dict_model["some_value_two"][0].items():
        assert isinstance(value, list)
        assert isinstance(key, str)
        for item in value:
            assert isinstance(item, dict)
            for key_2, value_2 in item.items():
                assert isinstance(key_2, str)
                assert isinstance(value_2, str)


async def test_cast_to_string_complex_types_datatime(create_model):
    class TestModel(BaseModel):
        some_value: datetime.datetime

    model = await create_model(TestModel)
    dict_model = model.to_dict()

    assert isinstance(dict_model["some_value"], float)


async def test_cast_to_string_complex_types_datatime_with_deciphering(create_model):
    class TestModel(BaseModel):
        some_value: datetime.datetime

    model = await create_model(TestModel)
    dict_model = model.to_dict(show_secrets=True)

    assert isinstance(dict_model["some_value"], float)


async def test_model_reduction(create_model):
    class TestModel(BaseModel):
        some_value: int

    model = await create_model(TestModel)
    dict_model = model.to_dict(values={"reduction": "reduction"})
    assert dict_model["reduction"] == "reduction"

    with pytest.raises(KeyError):
        _ = dict_model["some_value"]


async def test_model_reduction_with_deciphering(create_model):
    class TestModel(BaseModel):
        some_value: pydantic.SecretStr

    model = await create_model(TestModel)
    dict_model = model.to_dict(values={"reduction": "reduction"}, show_secrets=True)
    assert dict_model["reduction"] == "reduction"


# TODO: Добавить бенчмарки для to_dict.
#   Есть ощущение, что тут происходит много лишних операций.
