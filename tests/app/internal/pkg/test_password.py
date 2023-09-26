"""Test password module."""

import pydantic
import pytest

from app.internal.pkg.password import password


@pytest.mark.parametrize(
    "raw_password",
    [
        pydantic.SecretBytes(b"qzC9L&gC@RAJu@ve"),
        pydantic.SecretBytes(b"Z4xzgQtLsmDAHNs*"),
        pydantic.SecretBytes(b"dFSkX%Kn3+DRYAjA"),
        pydantic.SecretBytes(b"u^m^3S8MC6!(u8V6"),
        pydantic.SecretBytes(b"@ar!nV6CNq2S!IPc"),
    ],
)
def test_correct_password(raw_password: pydantic.SecretBytes):
    crypt_password = password.crypt_password(password=raw_password.get_secret_value())
    assert password.check_password(
        password=raw_password,
        hashed=pydantic.SecretBytes(crypt_password),
    )
