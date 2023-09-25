from __future__ import annotations

import time
import typing
from datetime import date, datetime
from typing import Any, Dict, List, Tuple, Type, TypeVar
from uuid import UUID

import pydantic
from jsf import JSF
from pydantic import UUID4

from app.pkg.models import types

__all__ = ["BaseModel", "Model"]

Model = TypeVar("Model", bound="BaseModel")
_T = TypeVar("_T")


class BaseModel(pydantic.BaseModel):
    """Base model for all models in API server."""

    def to_dict(
        self,
        show_secrets: bool = False,
        values: Dict[Any, Any] = None,
        **kwargs,
    ) -> Dict[Any, Any]:
        """Make a representation model from a class object to Dict object.

        Args:
            show_secrets:
                bool.
                default False.
                Shows secret in dict an object if True.
            values:
                Using an object to write to a Dict object.
            **kwargs:
                Optional arguments to be passed to the Dict object.

        Examples:
            If you don't want to show secret in a dict object,
            then you shouldn't use ``show_secrets`` argument::

                >>> from app.pkg.models.base import BaseModel
                >>> class TestModel(BaseModel):
                ...     some_value: pydantic.SecretStr
                ...     some_value_two: pydantic.SecretBytes
                >>> model = TestModel(some_value="key", some_value_two="value")
                >>> assert isinstance(model.some_value, pydantic.SecretStr)
                >>> assert isinstance(model.some_value_two, pydantic.SecretBytes)
                >>> dict_model = model.to_dict()
                >>> assert isinstance(dict_model["some_value"], str)
                >>> assert isinstance(dict_model["some_value_two"], str)
                >>> print(dict_model["some_value"])
                '**********'
                >>> print(dict_model["some_value_two"])
                '**********'

            If you want to deciphe sensitivity in a dict object,
            then you should use ``show_secrets`` argument::

                >>> from app.pkg.models.base import BaseModel
                >>> class TestModel(BaseModel):
                ...     some_value: pydantic.SecretStr
                ...     some_value_two: pydantic.SecretBytes
                >>> model = TestModel(some_value="key", some_value_two="value")
                >>> assert isinstance(model.some_value, pydantic.SecretStr)
                >>> assert isinstance(model.some_value_two, pydantic.SecretBytes)
                >>> dict_model = model.to_dict(show_secrets=True)
                >>> assert isinstance(dict_model["some_value"], str)
                >>> assert isinstance(dict_model["some_value_two"], str)
                >>> print(dict_model["some_value"])
                'key'
                >>> print(dict_model["some_value_two"])
                'value'

            In such cases, you can use the ``values`` argument for revrite values in
            a dict object::

                >>> from app.pkg.models.base import BaseModel
                >>> class TestModel(BaseModel):
                ...     some_value: pydantic.SecretStr
                ...     some_value_two: pydantic.SecretBytes
                >>> model = TestModel(some_value="key", some_value_two="value")
                >>> assert isinstance(model.some_value, pydantic.SecretStr)
                >>> assert isinstance(model.some_value_two, pydantic.SecretBytes)
                >>> dict_model = model.to_dict(show_secrets=True, values={"some_value": "value"})
                >>> assert isinstance(dict_model["some_value"], str)
                >>> assert isinstance(dict_model["some_value_two"], str)
                >>> print(dict_model["some_value"])
                'value'
                >>> print(dict_model["some_value_two"])
                'value'

        Raises:
            TypeError: If ``values`` are not a Dict object.

        Returns:
            Dict object with reveal password filed.
        """

        values = self.dict(**kwargs).items() if not values else values.items()
        r = {}
        for k, v in values:
            v = self.__cast_values(v=v, show_secrets=show_secrets)
            r[k] = v
        return r

    def __cast_values(self, v: _T, show_secrets: bool, **kwargs) -> _T:
        """Cast value for dict object.

        Args:
            v:
                Any value.
            show_secrets:
                If True, then the secret will be revealed.

        Warnings:
            This method is not memory optimized.
        """

        if isinstance(v, (List, Tuple)):
            return [
                self.__cast_values(v=ve, show_secrets=show_secrets, **kwargs) for ve in v
            ]

        elif isinstance(v, (pydantic.SecretBytes, pydantic.SecretStr)):
            return self.__cast_secret(v=v, show_secrets=show_secrets)

        elif isinstance(v, Dict) and v:
            return self.to_dict(show_secrets=show_secrets, values=v, **kwargs)

        elif isinstance(v, UUID) or isinstance(v, UUID4):
            return v.__str__()

        elif isinstance(v, datetime):
            return v.timestamp()

        return v

    @staticmethod
    def __cast_secret(v, show_secrets: bool) -> str:
        """Cast secret value to str.

        Args:
            v: pydantic.Secret* object.
            show_secrets: bool value. If True, then the secret will be revealed.

        Returns: str value of ``v``.
        """

        if isinstance(v, pydantic.SecretBytes):
            return v.get_secret_value().decode() if show_secrets else str(v)
        elif isinstance(v, pydantic.SecretStr):
            return v.get_secret_value() if show_secrets else str(v)

    def delete_attribute(self, attr: str) -> BaseModel:
        """Delete some attribute field from a model.

        Args:
            attr:
                name of field.

        Returns:
            self object.
        """

        delattr(self, attr)
        return self

    def migrate(
        self,
        model: Type[BaseModel],
        match_keys: typing.Dict[str, str] = None,
        random_fill: bool = False,
        extra_fields: typing.Dict[str, typing.Any] = None,
    ) -> Model:
        """Migrate one model to another ignoring missmatch.

        Args:
            model:
                Heir BaseModel object.
            random_fill:
                If True, then the fields that are not in the
                model will be filled with random values.
            match_keys:
                The keys of this object are the names of the
                fields of the model to which the migration will be made, and the
                values are the names of the fields of the current model.
                Key: name of field in self-model.
                Value: name of field in a target model.
            extra_fields:
                The keys of this object are the names of the
                fields of the model to which the migration will be made, and the
                values are the values of the fields of the current model.

                Key: name of field in a target model.

                Value: value of field in a target model.

        Examples:
            When migrating from model A to model B, the fields that are not
            in model B will be filled with them::

                >>> class A(BaseModel):
                ...     a: int
                ...     b: int
                ...     c: int
                ...     d: int
                >>> class B(BaseModel):
                ...     a: int
                ...     b: int
                ...     c: int
                >>> a = A(a=1, b=2, c=3, d=4)
                >>> a.migrate(model=B)  # B(a=1, b=2, c=3)

            But if you need to fill in the missing fields with a random value,
            then you can use the ``random_fill`` argument::

                >>> class A(BaseModel):
                ...     a: int
                ...     b: int
                ...     c: int
                >>> class B(BaseModel):
                ...     a: int
                ...     aa: int
                ...     b: int
                ...     c: int
                >>> a = A(a=1, b=2, c=3)
                >>> a.migrate(model=B, random_fill=True)  # B(a=1, aa=1011, b=2, c=3)

            If you need to migrate fields with different names, then you can use
            the ``match_keys`` argument::

                >>> class A(BaseModel):
                ...     a: int
                ...     b: int
                ...     c: int
                >>> class B(BaseModel):
                ...     aa: int
                ...     b: int
                ...     c: int
                >>> a = A(a=1, b=2, c=3)
                >>> a.migrate(model=B, match_keys={"aa": "a"})  # B(aa=1, b=2, c=3)

        Returns:
            pydantic model parsed from ``model``.
        """

        self_dict_model = self.to_dict(show_secrets=True)

        if not match_keys:
            match_keys = {}
        if not extra_fields:
            extra_fields = {}

        for key, value in match_keys.items():
            self_dict_model[key] = self_dict_model.pop(value)

        for key, value in extra_fields.items():
            self_dict_model[key] = value

        if not random_fill:
            return pydantic.parse_obj_as(model, self_dict_model)

        # TODO: Make this look better.
        faker = JSF(model.schema()).generate()
        faker.update(self_dict_model)
        return pydantic.parse_obj_as(model, faker)

    class Config:
        """Pydantic config class.

        See Also:
            https://pydantic-docs.helpmanual.io/usage/model_config/
        """

        # Use enum values instead of names.
        use_enum_values = True

        # Specify custom json encoders.
        json_encoders = {
            pydantic.SecretStr: lambda v: v.get_secret_value() if v else None,
            pydantic.SecretBytes: lambda v: v.get_secret_value() if v else None,
            types.EncryptedSecretBytes: lambda v: v.get_secret_value() if v else None,
            bytes: lambda v: v.decode() if v else None,
            datetime: lambda v: int(v.timestamp()) if v else None,
            date: lambda v: int(time.mktime(v.timetuple())) if v else None,
        }

        # Allow creating new fields in model.
        allow_population_by_field_name = True

        # Allow validate assignment.
        validate_assignment = True
