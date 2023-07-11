from __future__ import annotations

import time
from datetime import date, datetime
from typing import Any, Dict, List, Tuple, Type, TypeVar

import pydantic
from jsf import JSF
from pydantic import UUID4

from app.pkg.models import types

__all__ = ["BaseModel", "Model"]

Model = TypeVar("Model", bound="BaseModel")


class BaseModel(pydantic.BaseModel):
    """Base model for all models in project."""

    def to_dict(
        self,
        show_secrets: bool = False,
        values: Dict[Any, Any] = None,
        **kwargs,
    ) -> Dict[Any, Any]:
        """Make transfer model to Dict object.

        Args:
            show_secrets: bool. default False. Shows secret in dict object if True.
            values: Using an object to write to a Dict object.
        Keyword Args:
            Optional arguments to be passed to the Dict object.

        Returns: Dict object with reveal password filed.
        """

        values = self.dict(**kwargs).items() if not values else values.items()
        r = {}
        for k, v in values:
            v = self.__cast_value(v=v, show_secrets=show_secrets)
            r[k] = v
        return r

    def __cast_value(self, v, show_secrets, **kwargs):
        """Cast value to Dict object.

        Warnings:
            This method is not memory optimized.
        """

        if isinstance(v, List) or isinstance(v, Tuple):
            return [
                self.__cast_value(v=ve, show_secrets=show_secrets, **kwargs) for ve in v
            ]
        elif isinstance(v, pydantic.SecretBytes):
            return v.get_secret_value().decode() if show_secrets else str(v)
        elif isinstance(v, pydantic.SecretStr):
            return v.get_secret_value() if show_secrets else str(v)
        elif isinstance(v, Dict) and v:
            return self.to_dict(show_secrets=show_secrets, values=v, **kwargs)
        elif isinstance(v, UUID4):
            return v.__str__()
        elif isinstance(v, datetime):
            return v.timestamp()

        return v

    def delete_attribute(self, attr: str) -> BaseModel:
        """Delete `attr` field from model.

        Args:
            attr: str value, implements name of field.

        Returns: self object.
        """

        delattr(self, attr)
        return self

    def migrate(self, model: Type[BaseModel], random_fill: bool = False) -> Model:
        """Migrate one model to another ignoring missmatch.

        Args:
            random_fill: bool value. If True, then the fields that are not in the
                model will be filled with random values.
            model: Heir BaseModel object.

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

            But if you need to fill in the missing fields with a pattern,
                then you can use the ``fill_patter`` argument::
                >>> class A(BaseModel):
                ...     a: int
                ...     b: int
                ...     c: int
                >>> class B(BaseModel):
                ...     aa: int
                ...     b: int
                >>> a = A(a=1, b=2, c=3)
                >>> a.migrate(model=B, random_fill=True)  # B(aa=1011, b=2)

        Returns:
            pydantic model parsed from ``model``.
        """
        if not random_fill:
            return pydantic.parse_obj_as(model, self.to_dict(show_secrets=True))

        # TODO: Make this look better.
        faker = JSF(model.schema()).generate()
        faker.update(self.to_dict(show_secrets=True))
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
