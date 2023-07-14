import typing
from functools import partial

from polyfactory.value_generators.primitives import create_random_bytes

from app.pkg.models.types import EncryptedSecretBytes, NotEmptySecretStr
from app.pkg.models.types.strings import NotEmptyStr

T = typing.TypeVar("T")


__all__ = ["TypeProviders"]


class TypeProviders:
    @classmethod
    def provider_map(
        cls, faker_instance: typing.Type[T]
    ) -> typing.Dict[typing.Type, typing.Callable]:
        """Create a provider map for the given class.

        Warnings:
            Class must have a __faker__ attribute. This is a Faker instance.

        Args:
            faker_instance: Faker instance.

        Returns: Provider map.
        """

        return {
            NotEmptySecretStr: lambda: faker_instance.pystr(),
            NotEmptyStr: lambda: faker_instance.pystr(),
            EncryptedSecretBytes: lambda: partial(
                create_random_bytes, faker_instance.__random__
            ),
        }
