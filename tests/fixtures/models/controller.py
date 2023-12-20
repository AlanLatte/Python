"""Model controller fixtures."""

import typing
from typing import Any, Callable, Coroutine

import pydantic
import pytest
from jsf import JSF

from app.pkg.models.base import Model


@pytest.fixture()
def create_model() -> Callable[..., Coroutine[Any, Any, Model]]:
    """Create model with random data."""

    async def _create_model(model: typing.Type[Model], **kwargs) -> Model:
        """Create model with random data.

        Args:
            model: model for fill with random data.
            **kwargs: additional fields for model.

        Examples:
            When you need to create a model with random data, you can this fixture like
            this::
                >>> from app.pkg import models
                >>> from app.internal.repository.postgresql import UserRepository
                >>> async def test_correct(
                ...     create_model, user_repository: UserRepository
                ... ):
                ...     cmd = await create_model(models.CreateUserCommand)
                ...     user = await user_repository.create(cmd=cmd)
                ...     assert user.username == cmd.username

            If you have a model with additional fields, you can pass them to the
            fixture::
                >>> from app.pkg import models
                >>> from app.internal.repository.postgresql import UserRepository
                >>> async def test_correct(
                ...    create_model, user_repository: UserRepository
                ... ):
                ...     cmd = await create_model(
                ...         models.CreateUserCommand,
                ...         username="test@example.ru"
                ...     )
                ...     user = await user_repository.create(cmd=cmd)
                ...     assert user.username == cmd.username

        Warnings:
            This function on the fly creates a model with random data. This means
            that the model will not be validated for determining the uniqueness of
            the fields and determination of the correct data type. This is due to the
            fact that the model is created with random data, and it is impossible to
            determine whether the data is unique or not.

        Returns:
            Model with random data.
        """

        mock_model = JSF(model.schema()).generate()

        if kwargs:
            mock_model.update(kwargs)

        return pydantic.parse_obj_as(model, mock_model)

    return _create_model
