"""Generators for models."""

from typing import Any, Callable, Type

import pydantic
import pytest
from jsf import JSF

from app.pkg import models
from app.pkg.models.base import Model


def __generator(model: Type[Model], **kwargs) -> Callable[..., Model]:
    mock = JSF(model.schema())

    def generate() -> Any:
        mock_generate = mock.generate()
        mock_generate.update(kwargs)
        return pydantic.parse_obj_as(model, mock_generate)

    return generate()


@pytest.fixture()
def country_generator() -> Callable[[], Any]:
    return lambda **kwargs: __generator(models.Country, **kwargs)


@pytest.fixture()
def city_generator() -> Callable[[], Any]:
    return lambda **kwargs: __generator(models.City, **kwargs)


@pytest.fixture()
def contact_generator() -> Callable[[], Any]:
    return lambda **kwargs: __generator(models.Contacts, **kwargs)


@pytest.fixture()
def direction_generator() -> Callable[[], Any]:
    return lambda **kwargs: __generator(models.Direction, **kwargs)


@pytest.fixture()
def skill_generator() -> Callable[[], Any]:
    return lambda **kwargs: __generator(models.Skill, **kwargs)


@pytest.fixture()
def skill_level_generator() -> Callable[[], Any]:
    return lambda **kwargs: __generator(models.SkillLevel, **kwargs)


@pytest.fixture()
def partner_generator() -> Callable[[], Any]:
    return lambda **kwargs: __generator(models.Partner, **kwargs)
